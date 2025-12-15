"""
Test Suite for Algo5 Suggester
Bộ test bao phủ tất cả trường hợp cho thuật toán gợi ý địa điểm du lịch
"""
import pytest
from datetime import datetime, timedelta
from core.algo5.algo5_suggester import suggest_places, haversine


class TestHaversineDistance:
    """Test tính khoảng cách Haversine"""
    
    def test_tc01_same_location(self):
        """TC01: Khoảng cách giữa 2 điểm giống nhau phải bằng 0"""
        dist = haversine(10.7769, 106.7009, 10.7769, 106.7009)
        assert dist == 0, "Khoảng cách giữa cùng một điểm phải bằng 0"
    
    def test_tc02_known_distance(self):
        """TC02: Khoảng cách giữa 2 điểm đã biết (Sài Gòn - Hà Nội ~1160km)"""
        # Sài Gòn: 10.7769, 106.7009
        # Hà Nội: 21.0285, 105.8542
        dist = haversine(10.7769, 106.7009, 21.0285, 105.8542)
        assert 1100 < dist < 1200, f"Khoảng cách SG-HN phải ~1160km, nhận được {dist}km"
    
    def test_tc03_short_distance(self):
        """TC03: Khoảng cách ngắn trong thành phố (~1-2km)"""
        dist = haversine(10.7769, 106.7009, 10.7850, 106.7100)
        assert 0 < dist < 5, "Khoảng cách ngắn trong thành phố phải < 5km"
    
    def test_tc04_negative_coordinates(self):
        """TC04: Tọa độ âm (bán cầu nam/tây)"""
        dist = haversine(-33.8688, 151.2093, -37.8136, 144.9631)  # Sydney - Melbourne
        assert dist > 0, "Khoảng cách với tọa độ âm phải > 0"


class TestSuggestPlacesBasic:
    """Test chức năng cơ bản của suggest_places"""
    
    @pytest.fixture
    def sample_pois(self):
        """Dữ liệu POI mẫu cho test"""
        return [
            {
                "id": 1,
                "name": "Nhà thờ Đức Bà",
                "lat": 10.7797,
                "lon": 106.6991,
                "category": "religion",
                "rating": 4.5,
                "cost": 0,
                "open_hour": 8,
                "close_hour": 17
            },
            {
                "id": 2,
                "name": "Bảo tàng Chứng tích Chiến tranh",
                "lat": 10.7796,
                "lon": 106.6918,
                "category": "museum",
                "rating": 4.6,
                "cost": 40000,
                "open_hour": 7,
                "close_hour": 18
            },
            {
                "id": 3,
                "name": "Chợ Bến Thành",
                "lat": 10.7729,
                "lon": 106.6981,
                "category": "shopping",
                "rating": 4.2,
                "cost": 0,
                "open_hour": 6,
                "close_hour": 22
            }
        ]
    
    def test_tc05_normal_case(self, sample_pois):
        """TC05: Trường hợp bình thường với đủ thời gian và ngân sách"""
        current_loc = (10.7769, 106.7009)
        current_time = datetime(2025, 11, 30, 9, 0)
        end_time = datetime(2025, 11, 30, 18, 0)
        budget_left = 500000
        K = 3
        prefs = {"museum": 0.8, "religion": 0.6, "shopping": 0.4}
        
        results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, sample_pois)
        
        assert len(results) > 0, "Phải có ít nhất 1 gợi ý"
        assert len(results) <= K, f"Số lượng gợi ý không vượt quá K={K}"
    
    def test_tc06_zero_budget(self, sample_pois):
        """TC06: Ngân sách = 0, chỉ gợi ý POI miễn phí"""
        current_loc = (10.7769, 106.7009)
        current_time = datetime(2025, 11, 30, 9, 0)
        end_time = datetime(2025, 11, 30, 18, 0)
        budget_left = 0
        K = 5
        prefs = {"museum": 0.8, "religion": 0.6, "shopping": 0.4}
        
        results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, sample_pois)
        
        for r in results:
            assert r["poi"]["cost"] == 0, "Với budget=0, chỉ gợi ý POI miễn phí"
    
    def test_tc07_very_short_time(self, sample_pois):
        """TC07: Thời gian rất ngắn (30 phút)"""
        current_loc = (10.7769, 106.7009)
        current_time = datetime(2025, 11, 30, 9, 0)
        end_time = datetime(2025, 11, 30, 9, 30)  # Chỉ 30 phút
        budget_left = 500000
        K = 5
        prefs = {"museum": 0.8, "religion": 0.6, "shopping": 0.4}
        
        results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, sample_pois)
        
        # Có thể không có gợi ý nào do thời gian quá ngắn
        assert len(results) >= 0, "Kết quả phải là danh sách (có thể rỗng)"
    
    def test_tc08_all_pois_closed(self, sample_pois):
        """TC08: Tất cả POI đều đóng cửa"""
        current_loc = (10.7769, 106.7009)
        current_time = datetime(2025, 11, 30, 23, 0)  # 11 PM
        end_time = datetime(2025, 11, 30, 23, 59)
        budget_left = 500000
        K = 5
        prefs = {"museum": 0.8, "religion": 0.6, "shopping": 0.4}
        
        results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, sample_pois)
        
        assert len(results) == 0, "Không có gợi ý khi tất cả POI đóng cửa"


class TestSuggestPlacesEdgeCases:
    """Test các trường hợp biên"""
    
    @pytest.fixture
    def sample_pois(self):
        return [
            {
                "id": 1, "name": "POI A", "lat": 10.7797, "lon": 106.6991,
                "category": "food", "rating": 4.5, "cost": 50000,
                "open_hour": 8, "close_hour": 20
            },
            {
                "id": 2, "name": "POI B", "lat": 10.7850, "lon": 106.7050,
                "category": "park", "rating": 4.0, "cost": 0,
                "open_hour": 6, "close_hour": 22
            }
        ]
    
    def test_tc09_k_greater_than_pois(self, sample_pois):
        """TC09: K lớn hơn số lượng POI khả dụng"""
        current_loc = (10.7769, 106.7009)
        current_time = datetime(2025, 11, 30, 9, 0)
        end_time = datetime(2025, 11, 30, 18, 0)
        budget_left = 500000
        K = 100  # Lớn hơn số POI
        prefs = {"food": 0.8, "park": 0.6}
        
        results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, sample_pois)
        
        assert len(results) <= len(sample_pois), "Số gợi ý không vượt quá số POI"
    
    def test_tc10_k_equals_zero(self, sample_pois):
        """TC10: K = 0"""
        current_loc = (10.7769, 106.7009)
        current_time = datetime(2025, 11, 30, 9, 0)
        end_time = datetime(2025, 11, 30, 18, 0)
        budget_left = 500000
        K = 0
        prefs = {"food": 0.8, "park": 0.6}
        
        results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, sample_pois)
        
        assert len(results) == 0, "K=0 nên không có gợi ý"
    
    def test_tc11_empty_preferences(self, sample_pois):
        """TC11: Preferences rỗng"""
        current_loc = (10.7769, 106.7009)
        current_time = datetime(2025, 11, 30, 9, 0)
        end_time = datetime(2025, 11, 30, 18, 0)
        budget_left = 500000
        K = 5
        prefs = {}  # Rỗng
        
        results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, sample_pois)
        
        assert len(results) >= 0, "Vẫn hoạt động với preferences rỗng"
    
    def test_tc12_very_far_location(self, sample_pois):
        """TC12: Vị trí hiện tại rất xa (Hà Nội)"""
        current_loc = (21.0285, 105.8542)  # Hà Nội
        current_time = datetime(2025, 11, 30, 9, 0)
        end_time = datetime(2025, 11, 30, 18, 0)
        budget_left = 500000
        K = 5
        prefs = {"food": 0.8, "park": 0.6}
        
        results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, sample_pois)
        
        # Vì quá xa nên không thể đi bộ đến kịp
        assert len(results) == 0, "Vị trí quá xa không thể đến trong thời gian cho phép"


class TestSuggestPlacesScoring:
    """Test logic tính điểm và sắp xếp"""
    
    @pytest.fixture
    def diverse_pois(self):
        return [
            {
                "id": 1, "name": "Gần & Rating cao", "lat": 10.7770, "lon": 106.7010,
                "category": "museum", "rating": 5.0, "cost": 50000,
                "open_hour": 8, "close_hour": 20
            },
            {
                "id": 2, "name": "Xa & Rating thấp", "lat": 10.8500, "lon": 106.8000,
                "category": "museum", "rating": 3.0, "cost": 30000,
                "open_hour": 8, "close_hour": 20
            },
            {
                "id": 3, "name": "Trung bình", "lat": 10.7850, "lon": 106.7100,
                "category": "museum", "rating": 4.0, "cost": 40000,
                "open_hour": 8, "close_hour": 20
            }
        ]
    
    def test_tc13_closer_poi_higher_score(self, diverse_pois):
        """TC13: POI gần hơn có điểm cao hơn (với rating tương đương)"""
        current_loc = (10.7769, 106.7009)
        current_time = datetime(2025, 11, 30, 9, 0)
        end_time = datetime(2025, 11, 30, 18, 0)
        budget_left = 500000
        K = 3
        prefs = {"museum": 1.0}
        
        results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, diverse_pois)
        
        # POI đầu tiên phải là POI gần nhất và rating cao nhất
        if len(results) > 0:
            assert results[0]["poi"]["id"] == 1, "POI gần nhất và rating cao nhất phải được ưu tiên"
    
    def test_tc14_high_rating_prioritized(self, diverse_pois):
        """TC14: Rating cao được ưu tiên"""
        current_loc = (10.7769, 106.7009)
        current_time = datetime(2025, 11, 30, 9, 0)
        end_time = datetime(2025, 11, 30, 18, 0)
        budget_left = 500000
        K = 3
        prefs = {"museum": 1.0}
        
        results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, diverse_pois)
        
        # Kiểm tra kết quả được sắp xếp theo điểm giảm dần
        scores = [r["score"] for r in results]
        assert scores == sorted(scores, reverse=True), "Kết quả phải được sắp xếp theo điểm giảm dần"
    
    def test_tc15_preference_affects_score(self):
        """TC15: Preference ảnh hưởng đến điểm"""
        pois = [
            {
                "id": 1, "name": "Museum", "lat": 10.7770, "lon": 106.7010,
                "category": "museum", "rating": 4.0, "cost": 50000,
                "open_hour": 8, "close_hour": 20
            },
            {
                "id": 2, "name": "Park", "lat": 10.7770, "lon": 106.7010,
                "category": "park", "rating": 4.0, "cost": 0,
                "open_hour": 8, "close_hour": 20
            }
        ]
        
        current_loc = (10.7769, 106.7009)
        current_time = datetime(2025, 11, 30, 9, 0)
        end_time = datetime(2025, 11, 30, 18, 0)
        budget_left = 500000
        K = 2
        prefs = {"museum": 1.0, "park": 0.1}  # Ưu tiên museum
        
        results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, pois)
        
        if len(results) > 0:
            # Museum phải có điểm cao hơn park
            museum_score = next((r["score"] for r in results if r["poi"]["category"] == "museum"), None)
            park_score = next((r["score"] for r in results if r["poi"]["category"] == "park"), None)
            
            if museum_score and park_score:
                assert museum_score > park_score, "POI với preference cao hơn phải có điểm cao hơn"


class TestSuggestPlacesTimeConstraints:
    """Test ràng buộc thời gian"""
    
    @pytest.fixture
    def time_sensitive_pois(self):
        return [
            {
                "id": 1, "name": "Mở sáng sớm", "lat": 10.7770, "lon": 106.7010,
                "category": "food", "rating": 4.0, "cost": 50000,
                "open_hour": 6, "close_hour": 10  # Chỉ mở sáng
            },
            {
                "id": 2, "name": "Mở cả ngày", "lat": 10.7780, "lon": 106.7020,
                "category": "park", "rating": 4.0, "cost": 0,
                "open_hour": 0, "close_hour": 23
            },
            {
                "id": 3, "name": "Mở chiều tối", "lat": 10.7790, "lon": 106.7030,
                "category": "entertainment", "rating": 4.5, "cost": 100000,
                "open_hour": 18, "close_hour": 23
            }
        ]
    
    def test_tc16_morning_time_filter(self, time_sensitive_pois):
        """TC16: Lọc theo giờ mở cửa buổi sáng"""
        current_loc = (10.7769, 106.7009)
        current_time = datetime(2025, 11, 30, 7, 0)  # 7 AM
        end_time = datetime(2025, 11, 30, 9, 0)
        budget_left = 500000
        K = 5
        prefs = {"food": 1.0, "park": 1.0, "entertainment": 1.0}
        
        results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, time_sensitive_pois)
        
        # Chỉ có POI mở sáng và mở cả ngày
        for r in results:
            assert r["poi"]["id"] in [1, 2], "Chỉ gợi ý POI đang mở cửa vào buổi sáng"
    
    def test_tc17_evening_time_filter(self, time_sensitive_pois):
        """TC17: Lọc theo giờ mở cửa buổi tối"""
        current_loc = (10.7769, 106.7009)
        current_time = datetime(2025, 11, 30, 19, 0)  # 7 PM
        end_time = datetime(2025, 11, 30, 22, 0)
        budget_left = 500000
        K = 5
        prefs = {"food": 1.0, "park": 1.0, "entertainment": 1.0}
        
        results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, time_sensitive_pois)
        
        # Chỉ có POI mở tối và mở cả ngày
        for r in results:
            assert r["poi"]["id"] in [2, 3], "Chỉ gợi ý POI đang mở cửa vào buổi tối"
    
    def test_tc18_end_time_constraint(self):
        """TC18: Không gợi ý POI không thể đến kịp trước end_time"""
        pois = [
            {
                "id": 1, "name": "POI gần", "lat": 10.7770, "lon": 106.7010,
                "category": "museum", "rating": 4.0, "cost": 0,
                "open_hour": 8, "close_hour": 20
            }
        ]
        
        current_loc = (10.7769, 106.7009)
        current_time = datetime(2025, 11, 30, 17, 55)  # 5:55 PM
        end_time = datetime(2025, 11, 30, 18, 0)  # 6:00 PM (chỉ còn 5 phút)
        budget_left = 500000
        K = 5
        prefs = {"museum": 1.0}
        
        results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, pois)
        
        # Có thể không có gợi ý vì thời gian quá ngắn
        for r in results:
            arrival = r["poi"]
            # Nếu có gợi ý, phải đảm bảo đến được trước end_time
            assert current_time + timedelta(hours=r["travel_time_hours"]) <= end_time


class TestSuggestPlacesBudgetConstraints:
    """Test ràng buộc ngân sách"""
    
    def test_tc19_budget_filter_strict(self):
        """TC19: Lọc nghiêm ngặt theo ngân sách"""
        pois = [
            {"id": 1, "name": "Rẻ", "lat": 10.7770, "lon": 106.7010,
             "category": "museum", "rating": 4.0, "cost": 20000,
             "open_hour": 8, "close_hour": 20},
            {"id": 2, "name": "Đắt", "lat": 10.7780, "lon": 106.7020,
             "category": "museum", "rating": 5.0, "cost": 200000,
             "open_hour": 8, "close_hour": 20},
            {"id": 3, "name": "Miễn phí", "lat": 10.7790, "lon": 106.7030,
             "category": "park", "rating": 4.5, "cost": 0,
             "open_hour": 8, "close_hour": 20}
        ]
        
        current_loc = (10.7769, 106.7009)
        current_time = datetime(2025, 11, 30, 9, 0)
        end_time = datetime(2025, 11, 30, 18, 0)
        budget_left = 50000  # Chỉ đủ cho POI rẻ và miễn phí
        K = 5
        prefs = {"museum": 1.0, "park": 1.0}
        
        results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, pois)
        
        # Không được gợi ý POI đắt
        for r in results:
            assert r["poi"]["cost"] <= budget_left, f"POI cost {r['poi']['cost']} vượt quá budget {budget_left}"
    
    def test_tc20_negative_budget(self):
        """TC20: Ngân sách âm (edge case)"""
        pois = [
            {"id": 1, "name": "Miễn phí", "lat": 10.7770, "lon": 106.7010,
             "category": "park", "rating": 4.5, "cost": 0,
             "open_hour": 8, "close_hour": 20}
        ]
        
        current_loc = (10.7769, 106.7009)
        current_time = datetime(2025, 11, 30, 9, 0)
        end_time = datetime(2025, 11, 30, 18, 0)
        budget_left = -10000  # Ngân sách âm
        K = 5
        prefs = {"park": 1.0}
        
        results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, pois)
        
        # Không có gợi ý nào vì ngân sách âm
        assert len(results) == 0, "Ngân sách âm không được gợi ý POI nào"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
