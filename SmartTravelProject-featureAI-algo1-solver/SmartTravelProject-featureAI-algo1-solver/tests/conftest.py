"""
Pytest configuration and shared fixtures
"""
import pytest
import os
import shutil


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment before all tests"""
    # Create test data directory
    os.makedirs("tests/test_data", exist_ok=True)
    yield
    # Cleanup after all tests
    if os.path.exists("tests/test_data"):
        shutil.rmtree("tests/test_data")


@pytest.fixture
def sample_pois():
    """Fixture providing sample POI data"""
    return [
        {
            "id": 1,
            "name": "Sample POI 1",
            "lat": 10.7769,
            "lon": 106.7006,
            "open_hour": 8,
            "close_hour": 18,
            "visit_duration_min": 60,
            "entry_fee": 50000,
            "rating": 4.5,
            "tags": ["museum", "cultural"]
        },
        {
            "id": 2,
            "name": "Sample POI 2",
            "lat": 10.7829,
            "lon": 106.7106,
            "open_hour": 9,
            "close_hour": 20,
            "visit_duration_min": 45,
            "entry_fee": 30000,
            "rating": 4.0,
            "tags": ["park", "nature"]
        }
    ]
