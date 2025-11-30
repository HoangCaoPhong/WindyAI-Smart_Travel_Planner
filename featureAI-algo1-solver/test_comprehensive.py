"""
Comprehensive test suite with 20 test cases covering all scenarios
for Smart Travel Project AI Algorithm 1
"""
import pytest
import pandas as pd
from datetime import datetime, timedelta
from core.solver_route import load_pois, plan_route
from core.scorer import score_candidate, preference_score
from core.utils_geo import haversine_km, travel_info
from core.optimizer import two_opt, total_travel_time
from core.config import DEFAULT_START, DEFAULT_TIME_WINDOW, DEFAULT_BUDGET
import os


# ==================== UTILITY FUNCTIONS ====================
def create_test_csv(filename, pois_data):
    """Helper to create test CSV files"""
    df = pd.DataFrame(pois_data)
    os.makedirs("tests/test_data", exist_ok=True)
    df.to_csv(f"tests/test_data/{filename}", index=False)
    return f"tests/test_data/{filename}"


# ==================== GEO UTILS TESTS ====================
class TestGeoUtils:
    """Test cases 1-3: Geographic utilities"""
    
    def test_01_haversine_same_location(self):
        """TC01: Distance between same coordinates should be 0"""
        loc = (10.7769, 106.7006)
        distance = haversine_km(loc, loc)
        assert distance == 0.0
    
    def test_02_haversine_known_distance(self):
        """TC02: Validate known distance calculation"""
        # Ben Thanh Market to Notre Dame Cathedral (~1km)
        ben_thanh = (10.7729, 106.6981)
        notre_dame = (10.7797, 106.6991)
        distance = haversine_km(ben_thanh, notre_dame)
        assert 0.7 < distance < 1.0  # approximately 0.76 km
    
    def test_03_travel_info_all_modes(self):
        """TC03: Calculate travel info for all transportation modes"""
        loc_a = (10.7769, 106.7006)
        loc_b = (10.7829, 106.7106)
        
        for mode in ["walking", "motorbike", "taxi"]:
            dist, time, cost = travel_info(loc_a, loc_b, mode)
            assert dist > 0
            assert time > 0
            assert cost >= 0  # walking is free
            if mode == "walking":
                assert cost == 0.0


# ==================== SCORER TESTS ====================
class TestScorer:
    """Test cases 4-7: Scoring and preference matching"""
    
    def test_04_preference_score_perfect_match(self):
        """TC04: Perfect preference match should return 1.0"""
        tags = ["museum", "historical", "cultural"]
        prefs = ["museum", "historical", "cultural"]
        score = preference_score(tags, prefs)
        assert score == 1.0
    
    def test_05_preference_score_no_match(self):
        """TC05: No preference match should return 0.0"""
        tags = ["museum", "historical"]
        prefs = ["beach", "adventure"]
        score = preference_score(tags, prefs)
        assert score == 0.0
    
    def test_06_preference_score_partial_match(self):
        """TC06: Partial preference match"""
        tags = ["museum", "historical", "cultural", "art"]
        prefs = ["museum", "beach"]
        score = preference_score(tags, prefs)
        assert score == 0.5  # 1 out of 2 prefs matched
    
    def test_07_score_candidate_comparison(self):
        """TC07: Lower score for better candidates"""
        poi_high_rating = {
            "id": 1,
            "name": "Great Museum",
            "rating": 4.8,
            "tags": ["museum", "cultural"],
            "visit_duration_min": 60,
            "entry_fee": 50000
        }
        poi_low_rating = {
            "id": 2,
            "name": "Average Spot",
            "rating": 2.5,
            "tags": ["park"],
            "visit_duration_min": 60,
            "entry_fee": 0
        }
        
        prefs = ["museum", "cultural"]
        score_high = score_candidate(poi_high_rating, 10, 5000, prefs)
        score_low = score_candidate(poi_low_rating, 10, 5000, prefs)
        
        assert score_high < score_low  # better poi has lower score


# ==================== POI LOADING TESTS ====================
class TestPOILoading:
    """Test cases 8-10: POI data loading and validation"""
    
    def test_08_load_pois_valid_csv(self):
        """TC08: Load POIs from valid CSV"""
        pois_data = [
            {
                "id": 1, "name": "Museum A", "lat": 10.77, "lon": 106.70,
                "open_hour": 8, "close_hour": 18, "visit_duration_min": 60,
                "entry_fee": 50000, "rating": 4.5, "tags": "museum;cultural"
            },
            {
                "id": 2, "name": "Park B", "lat": 10.78, "lon": 106.71,
                "open_hour": 6, "close_hour": 22, "visit_duration_min": 30,
                "entry_fee": 0, "rating": 4.0, "tags": "park;nature"
            }
        ]
        csv_path = create_test_csv("test_pois.csv", pois_data)
        pois = load_pois(csv_path)
        
        assert len(pois) == 2
        assert pois[0]["tags"] == ["museum", "cultural"]
        assert pois[1]["tags"] == ["park", "nature"]
        assert pois[0]["visit_duration"] == 60
    
    def test_09_load_pois_empty_tags(self):
        """TC09: Handle POIs with empty tags"""
        pois_data = [
            {
                "id": 1, "name": "Place A", "lat": 10.77, "lon": 106.70,
                "open_hour": 8, "close_hour": 18, "visit_duration_min": 30,
                "entry_fee": 0, "rating": 3.5, "tags": ""
            }
        ]
        csv_path = create_test_csv("test_empty_tags.csv", pois_data)
        pois = load_pois(csv_path)
        
        assert pois[0]["tags"] == []
    
    def test_10_load_pois_type_conversion(self):
        """TC10: Ensure proper type conversion of POI fields"""
        pois_data = [
            {
                "id": 1, "name": "Test POI", "lat": "10.77", "lon": "106.70",
                "open_hour": "9", "close_hour": "17", "visit_duration_min": "45",
                "entry_fee": "25000.5", "rating": "4.2", "tags": "test"
            }
        ]
        csv_path = create_test_csv("test_types.csv", pois_data)
        pois = load_pois(csv_path)
        
        assert isinstance(pois[0]["lat"], float)
        assert isinstance(pois[0]["lon"], float)
        assert isinstance(pois[0]["open_hour"], int)
        assert isinstance(pois[0]["close_hour"], int)
        assert isinstance(pois[0]["entry_fee"], float)
        assert isinstance(pois[0]["rating"], float)


# ==================== ROUTE PLANNING TESTS ====================
class TestRoutePlanning:
    """Test cases 11-17: Core route planning algorithm"""
    
    def test_11_plan_route_basic(self):
        """TC11: Basic route planning with available POIs"""
        pois_data = [
            {
                "id": 1, "name": "POI A", "lat": 10.7769, "lon": 106.7006,
                "open_hour": 8, "close_hour": 20, "visit_duration_min": 60,
                "entry_fee": 50000, "rating": 4.5, "tags": "museum"
            },
            {
                "id": 2, "name": "POI B", "lat": 10.7829, "lon": 106.7106,
                "open_hour": 8, "close_hour": 20, "visit_duration_min": 45,
                "entry_fee": 30000, "rating": 4.0, "tags": "park"
            }
        ]
        csv_path = create_test_csv("test_basic_route.csv", pois_data)
        pois = load_pois(csv_path)
        
        route = plan_route(
            pois,
            user_prefs=["museum"],
            start_loc=(10.7769, 106.7006),
            time_window=("2025-12-01 09:00", "2025-12-01 18:00"),
            budget=500000
        )
        
        assert len(route) > 0
        assert all("name" in step for step in route)
        assert all("arrive_time" in step for step in route)
    
    def test_12_plan_route_budget_constraint(self):
        """TC12: Route planning with tight budget constraint"""
        pois_data = [
            {
                "id": 1, "name": "Expensive POI", "lat": 10.78, "lon": 106.70,
                "open_hour": 9, "close_hour": 18, "visit_duration_min": 60,
                "entry_fee": 200000, "rating": 5.0, "tags": "luxury"
            },
            {
                "id": 2, "name": "Free POI", "lat": 10.77, "lon": 106.71,
                "open_hour": 9, "close_hour": 18, "visit_duration_min": 30,
                "entry_fee": 0, "rating": 4.0, "tags": "park"
            }
        ]
        csv_path = create_test_csv("test_budget.csv", pois_data)
        pois = load_pois(csv_path)
        
        route = plan_route(
            pois,
            start_loc=(10.7769, 106.7006),
            time_window=("2025-12-01 09:00", "2025-12-01 18:00"),
            budget=50000  # tight budget
        )
        
        total_cost = sum(step["entry_fee"] + step["travel_cost"] for step in route)
        assert total_cost <= 50000
    
    def test_13_plan_route_time_constraint(self):
        """TC13: Route planning with tight time window"""
        pois_data = [
            {
                "id": 1, "name": "POI A", "lat": 10.78, "lon": 106.70,
                "open_hour": 9, "close_hour": 18, "visit_duration_min": 120,
                "entry_fee": 50000, "rating": 4.5, "tags": "museum"
            },
            {
                "id": 2, "name": "POI B", "lat": 10.79, "lon": 106.71,
                "open_hour": 9, "close_hour": 18, "visit_duration_min": 120,
                "entry_fee": 30000, "rating": 4.0, "tags": "park"
            }
        ]
        csv_path = create_test_csv("test_time.csv", pois_data)
        pois = load_pois(csv_path)
        
        route = plan_route(
            pois,
            start_loc=(10.7769, 106.7006),
            time_window=("2025-12-01 10:00", "2025-12-01 13:00"),  # 3 hours
            budget=500000
        )
        
        # Should not exceed time window
        if route:
            last_depart = route[-1]["depart_time"]
            end_time = datetime.strptime("2025-12-01 13:00", "%Y-%m-%d %H:%M")
            assert last_depart <= end_time
    
    def test_14_plan_route_opening_hours(self):
        """TC14: Respect POI opening hours"""
        pois_data = [
            {
                "id": 1, "name": "Morning POI", "lat": 10.78, "lon": 106.70,
                "open_hour": 6, "close_hour": 12, "visit_duration_min": 60,
                "entry_fee": 0, "rating": 4.0, "tags": "market"
            },
            {
                "id": 2, "name": "Evening POI", "lat": 10.79, "lon": 106.71,
                "open_hour": 18, "close_hour": 23, "visit_duration_min": 90,
                "entry_fee": 100000, "rating": 4.5, "tags": "restaurant"
            }
        ]
        csv_path = create_test_csv("test_hours.csv", pois_data)
        pois = load_pois(csv_path)
        
        # Plan for afternoon - should skip morning POI
        route = plan_route(
            pois,
            start_loc=(10.7769, 106.7006),
            time_window=("2025-12-01 14:00", "2025-12-01 22:00"),
            budget=500000
        )
        
        if route:
            # All POIs should be visited within their opening hours
            for step in route:
                arrive_hour = step["arrive_time"].hour
                depart_hour = step["depart_time"].hour
                # Find the POI from the data
                poi = next(p for p in pois if p["name"] == step["name"])
                assert arrive_hour >= poi["open_hour"]
                assert depart_hour <= poi["close_hour"]
    
    def test_15_plan_route_empty_pois(self):
        """TC15: Handle empty POI list"""
        route = plan_route(
            [],
            start_loc=(10.7769, 106.7006),
            time_window=("2025-12-01 09:00", "2025-12-01 18:00"),
            budget=500000
        )
        
        assert route == []
    
    def test_16_plan_route_no_feasible_pois(self):
        """TC16: Handle case where no POI meets constraints"""
        pois_data = [
            {
                "id": 1, "name": "Too Expensive", "lat": 10.78, "lon": 106.70,
                "open_hour": 9, "close_hour": 18, "visit_duration_min": 60,
                "entry_fee": 1000000, "rating": 5.0, "tags": "luxury"
            }
        ]
        csv_path = create_test_csv("test_infeasible.csv", pois_data)
        pois = load_pois(csv_path)
        
        route = plan_route(
            pois,
            start_loc=(10.7769, 106.7006),
            time_window=("2025-12-01 09:00", "2025-12-01 18:00"),
            budget=50000  # too low
        )
        
        assert route == []
    
    def test_17_plan_route_preference_priority(self):
        """TC17: Verify preferred POIs are prioritized"""
        pois_data = [
            {
                "id": 1, "name": "Preferred POI", "lat": 10.78, "lon": 106.70,
                "open_hour": 9, "close_hour": 18, "visit_duration_min": 60,
                "entry_fee": 50000, "rating": 4.0, "tags": "museum;historical"
            },
            {
                "id": 2, "name": "Non-Preferred POI", "lat": 10.77, "lon": 106.71,
                "open_hour": 9, "close_hour": 18, "visit_duration_min": 60,
                "entry_fee": 50000, "rating": 4.8, "tags": "shopping"
            }
        ]
        csv_path = create_test_csv("test_preference.csv", pois_data)
        pois = load_pois(csv_path)
        
        route = plan_route(
            pois,
            user_prefs=["museum", "historical"],
            start_loc=(10.7769, 106.7006),
            time_window=("2025-12-01 09:00", "2025-12-01 12:00"),
            budget=500000
        )
        
        # First POI should be the preferred one
        if len(route) > 0:
            assert "Preferred POI" in route[0]["name"]


# ==================== OPTIMIZER TESTS ====================
class TestOptimizer:
    """Test cases 18-19: Route optimization"""
    
    def test_18_two_opt_improvement(self):
        """TC18: 2-opt should improve or maintain route quality"""
        # Create a simple route with travel times
        route = [
            {"id": 1, "name": "A", "travel_time_min": 10},
            {"id": 2, "name": "B", "travel_time_min": 30},
            {"id": 3, "name": "C", "travel_time_min": 15},
            {"id": 4, "name": "D", "travel_time_min": 20}
        ]
        
        original_time = total_travel_time(route)
        optimized = two_opt(route)
        optimized_time = total_travel_time(optimized)
        
        # Optimized should be better or equal
        assert optimized_time <= original_time
    
    def test_19_two_opt_short_route(self):
        """TC19: 2-opt with route too short to optimize"""
        route = [
            {"id": 1, "name": "A", "travel_time_min": 10},
            {"id": 2, "name": "B", "travel_time_min": 15}
        ]
        
        optimized = two_opt(route)
        assert optimized == route  # should return unchanged


# ==================== INTEGRATION TEST ====================
class TestIntegration:
    """Test case 20: End-to-end integration"""
    
    def test_20_full_workflow_integration(self):
        """TC20: Complete workflow from CSV to optimized route"""
        # Create comprehensive test dataset
        pois_data = [
            {
                "id": 1, "name": "Ben Thanh Market", "lat": 10.7729, "lon": 106.6981,
                "open_hour": 7, "close_hour": 19, "visit_duration_min": 90,
                "entry_fee": 0, "rating": 4.5, "tags": "market;shopping;cultural"
            },
            {
                "id": 2, "name": "War Museum", "lat": 10.7797, "lon": 106.6918,
                "open_hour": 8, "close_hour": 17, "visit_duration_min": 120,
                "entry_fee": 40000, "rating": 4.7, "tags": "museum;historical;educational"
            },
            {
                "id": 3, "name": "Notre Dame Cathedral", "lat": 10.7797, "lon": 106.6991,
                "open_hour": 8, "close_hour": 18, "visit_duration_min": 45,
                "entry_fee": 0, "rating": 4.6, "tags": "historical;architectural;cultural"
            },
            {
                "id": 4, "name": "Coffee Apartment", "lat": 10.7824, "lon": 106.7010,
                "open_hour": 8, "close_hour": 22, "visit_duration_min": 60,
                "entry_fee": 50000, "rating": 4.4, "tags": "cafe;trendy;instagram"
            },
            {
                "id": 5, "name": "Saigon Opera House", "lat": 10.7770, "lon": 106.7035,
                "open_hour": 9, "close_hour": 20, "visit_duration_min": 75,
                "entry_fee": 150000, "rating": 4.8, "tags": "cultural;architectural;entertainment"
            }
        ]
        csv_path = create_test_csv("test_integration.csv", pois_data)
        
        # Load POIs
        pois = load_pois(csv_path)
        assert len(pois) == 5
        
        # Plan route with specific preferences
        route = plan_route(
            pois,
            user_prefs=["historical", "cultural", "museum"],
            start_loc=(10.7769, 106.7006),
            time_window=("2025-12-01 08:00", "2025-12-01 18:00"),
            budget=500000
        )
        
        # Verify route properties
        assert len(route) > 0
        
        # Check budget constraint
        total_cost = sum(step["entry_fee"] + step["travel_cost"] for step in route)
        assert total_cost <= 500000
        
        # Check time constraint
        start_time = datetime.strptime("2025-12-01 08:00", "%Y-%m-%d %H:%M")
        end_time = datetime.strptime("2025-12-01 18:00", "%Y-%m-%d %H:%M")
        assert route[0]["arrive_time"] >= start_time
        assert route[-1]["depart_time"] <= end_time
        
        # Check no duplicate visits
        visited_ids = [step["id"] for step in route]
        assert len(visited_ids) == len(set(visited_ids))
        
        # Check route continuity (depart time of step N < arrive time of step N+1)
        for i in range(len(route) - 1):
            assert route[i]["depart_time"] <= route[i+1]["arrive_time"]
        
        print(f"\n✓ Integration test passed: {len(route)} POIs in route")
        for step in route:
            print(f"  - {step['name']} ({step['mode']}): "
                  f"{step['arrive_time'].strftime('%H:%M')} - {step['depart_time'].strftime('%H:%M')}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
