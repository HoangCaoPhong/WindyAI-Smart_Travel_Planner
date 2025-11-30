#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST CASES - Chương trình tìm đường đi ngắn nhất
20 test cases bao phủ tất cả các module và trường hợp
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Import các module cần test
from config import NOMINATIM_URL, OSRM_URL, OPENWEATHER_URL
from geocoding import geocode
from routing import get_route_geometry, get_route_steps
from weather import get_weather
from mapping import create_single_vehicle_map, create_comparison_map
from ui import get_vehicle_choice, display_weather, display_route_steps, display_comparison_result


class TestConfig(unittest.TestCase):
    """Test cases cho module config.py"""
    
    def test_01_config_urls_not_empty(self):
        """TC01: Kiểm tra các URL API không rỗng"""
        self.assertIsNotNone(NOMINATIM_URL)
        self.assertIsNotNone(OSRM_URL)
        self.assertIsNotNone(OPENWEATHER_URL)
        self.assertTrue(len(NOMINATIM_URL) > 0)
        self.assertTrue(len(OSRM_URL) > 0)
        self.assertTrue(len(OPENWEATHER_URL) > 0)
    
    def test_02_config_urls_valid_format(self):
        """TC02: Kiểm tra format URL hợp lệ (https)"""
        self.assertTrue(NOMINATIM_URL.startswith('https://'))
        self.assertTrue(OSRM_URL.startswith('https://') or OSRM_URL.startswith('http://'))
        self.assertTrue(OPENWEATHER_URL.startswith('https://') or OPENWEATHER_URL.startswith('http://'))


class TestGeocoding(unittest.TestCase):
    """Test cases cho module geocoding.py"""
    
    @patch('geocoding.requests.get')
    @patch('geocoding.time.sleep')
    def test_03_geocode_valid_address(self, mock_sleep, mock_get):
        """TC03: Geocode với địa chỉ hợp lệ"""
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {
                'lat': '10.8231',
                'lon': '106.6297',
                'display_name': 'Ho Chi Minh City, Vietnam'
            }
        ]
        mock_get.return_value = mock_response
        
        lat, lon, name = geocode("Ho Chi Minh City")
        
        self.assertEqual(lat, 10.8231)
        self.assertEqual(lon, 106.6297)
        self.assertEqual(name, 'Ho Chi Minh City, Vietnam')
        mock_sleep.assert_called_once_with(1)
    
    @patch('geocoding.requests.get')
    @patch('geocoding.time.sleep')
    def test_04_geocode_empty_result(self, mock_sleep, mock_get):
        """TC04: Geocode trả về kết quả rỗng"""
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_get.return_value = mock_response
        
        with self.assertRaises(ValueError) as context:
            geocode("XYZ Invalid Address 123456")
        
        self.assertIn("Không tìm thấy địa chỉ", str(context.exception))
    
    @patch('geocoding.requests.get')
    @patch('geocoding.time.sleep')
    def test_05_geocode_network_error(self, mock_sleep, mock_get):
        """TC05: Geocode với lỗi mạng"""
        mock_get.side_effect = Exception("Network error")
        
        with self.assertRaises(Exception):
            geocode("Test Address")


class TestRouting(unittest.TestCase):
    """Test cases cho module routing.py"""
    
    @patch('routing.requests.get')
    def test_06_get_route_geometry_driving(self, mock_get):
        """TC06: Lấy geometry tuyến đường cho ô tô"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'routes': [{
                'geometry': {
                    'coordinates': [[106.6297, 10.8231], [105.8542, 21.0285]]
                },
                'distance': 1720000,  # 1720 km
                'duration': 61920     # 17.2 giờ
            }]
        }
        mock_get.return_value = mock_response
        
        geometry, km, hrs = get_route_geometry(106.6297, 10.8231, 105.8542, 21.0285, "driving")
        
        self.assertEqual(len(geometry), 2)
        self.assertAlmostEqual(km, 1720.0, places=1)
        self.assertAlmostEqual(hrs, 17.2, places=1)
    
    @patch('routing.requests.get')
    def test_07_get_route_geometry_bike(self, mock_get):
        """TC07: Lấy geometry tuyến đường cho xe máy"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'routes': [{
                'geometry': {
                    'coordinates': [[106.6297, 10.8231], [105.8542, 21.0285]]
                },
                'distance': 1735000,  # 1735 km
                'duration': 69400     # 19.3 giờ
            }]
        }
        mock_get.return_value = mock_response
        
        geometry, km, hrs = get_route_geometry(106.6297, 10.8231, 105.8542, 21.0285, "bike")
        
        self.assertEqual(len(geometry), 2)
        self.assertAlmostEqual(km, 1735.0, places=1)
        self.assertAlmostEqual(hrs, 19.3, places=1)
    
    @patch('routing.requests.get')
    def test_08_get_route_steps_with_instructions(self, mock_get):
        """TC08: Lấy chỉ dẫn từng bước"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'routes': [{
                'distance': 5000,
                'duration': 600,
                'legs': [{
                    'steps': [
                        {
                            'maneuver': {'instruction': 'Turn left'},
                            'name': 'Main Street',
                            'distance': 500
                        },
                        {
                            'maneuver': {'instruction': 'Turn right'},
                            'name': 'Second Avenue',
                            'distance': 300
                        }
                    ]
                }]
            }]
        }
        mock_get.return_value = mock_response
        
        result = get_route_steps(106.6297, 10.8231, 106.6500, 10.8400, "driving")
        
        self.assertEqual(result['distance_km'], 5.0)
        self.assertEqual(result['time_min'], 10)
        self.assertEqual(len(result['steps']), 2)
        self.assertEqual(result['steps'][0]['instruction'], 'Turn left')
        self.assertEqual(result['steps'][0]['street'], 'Main Street')
    
    @patch('routing.requests.get')
    def test_09_get_route_steps_missing_street_name(self, mock_get):
        """TC09: Chỉ dẫn không có tên đường"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'routes': [{
                'distance': 1000,
                'duration': 120,
                'legs': [{
                    'steps': [
                        {
                            'maneuver': {'instruction': 'Continue straight'},
                            'name': '',
                            'distance': 1000
                        }
                    ]
                }]
            }]
        }
        mock_get.return_value = mock_response
        
        result = get_route_steps(106.6297, 10.8231, 106.6500, 10.8400, "bike")
        
        self.assertEqual(result['steps'][0]['street'], '')


class TestWeather(unittest.TestCase):
    """Test cases cho module weather.py"""
    
    @patch('weather.requests.get')
    def test_10_get_weather_success(self, mock_get):
        """TC10: Lấy thông tin thời tiết thành công"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'main': {
                'temp': 28.5,
                'feels_like': 32.1,
                'humidity': 75
            },
            'weather': [{'description': 'scattered clouds'}],
            'wind': {'speed': 3.5}
        }
        mock_get.return_value = mock_response
        
        with patch('weather.OPENWEATHER_API_KEY', 'test_key_12345'):
            weather_data = get_weather(10.8231, 106.6297)
        
        self.assertIsNotNone(weather_data)
        self.assertEqual(weather_data['temp'], 28.5)
        self.assertEqual(weather_data['feels_like'], 32.1)
        self.assertEqual(weather_data['humidity'], 75)
        self.assertEqual(weather_data['description'], 'scattered clouds')
        self.assertEqual(weather_data['wind_speed'], 3.5)
    
    @patch('weather.OPENWEATHER_API_KEY', 'YOUR_API_KEY_HERE')
    def test_11_get_weather_no_api_key(self):
        """TC11: Không có API key hợp lệ"""
        weather_data = get_weather(10.8231, 106.6297)
        
        self.assertIsNone(weather_data)
    
    @patch('weather.requests.get')
    def test_12_get_weather_api_error(self, mock_get):
        """TC12: API trả về lỗi"""
        mock_get.side_effect = Exception("API Error")
        
        with patch('weather.OPENWEATHER_API_KEY', 'test_key'):
            weather_data = get_weather(10.8231, 106.6297)
        
        self.assertIsNone(weather_data)


class TestMapping(unittest.TestCase):
    """Test cases cho module mapping.py"""
    
    def test_13_create_single_vehicle_map_driving(self):
        """TC13: Tạo bản đồ cho ô tô"""
        geometry = [[106.6297, 10.8231], [106.7000, 10.9000]]
        output_file = "test_route_driving.html"
        
        result = create_single_vehicle_map(
            10.8231, 106.6297, 10.9000, 106.7000,
            "Start", "End",
            geometry, 50.5, 1.5,
            "driving", output_file
        )
        
        self.assertEqual(result, output_file)
        self.assertTrue(os.path.exists(output_file))
        
        # Cleanup
        if os.path.exists(output_file):
            os.remove(output_file)
    
    def test_14_create_single_vehicle_map_bike(self):
        """TC14: Tạo bản đồ cho xe máy"""
        geometry = [[106.6297, 10.8231], [106.7000, 10.9000]]
        output_file = "test_route_bike.html"
        
        result = create_single_vehicle_map(
            10.8231, 106.6297, 10.9000, 106.7000,
            "Start", "End",
            geometry, 52.0, 1.6,
            "bike", output_file
        )
        
        self.assertEqual(result, output_file)
        self.assertTrue(os.path.exists(output_file))
        
        # Cleanup
        if os.path.exists(output_file):
            os.remove(output_file)
    
    def test_15_create_comparison_map(self):
        """TC15: Tạo bản đồ so sánh"""
        geom_car = [[106.6297, 10.8231], [106.7000, 10.9000]]
        geom_bike = [[106.6297, 10.8231], [106.7100, 10.9100]]
        
        output_file, comparison = create_comparison_map(
            10.8231, 106.6297, 10.9000, 106.7000,
            "Start", "End",
            geom_car, 50.0, 1.5,
            geom_bike, 52.0, 1.6
        )
        
        self.assertEqual(output_file, "route_comparison.html")
        self.assertTrue(os.path.exists(output_file))
        self.assertIn('diff_km', comparison)
        self.assertIn('diff_min', comparison)
        self.assertIn('faster_vehicle', comparison)
        
        # Cleanup
        if os.path.exists(output_file):
            os.remove(output_file)
    
    def test_16_comparison_car_faster(self):
        """TC16: So sánh - Ô tô nhanh hơn"""
        geom = [[106.6297, 10.8231], [106.7000, 10.9000]]
        
        _, comparison = create_comparison_map(
            10.8231, 106.6297, 10.9000, 106.7000,
            "Start", "End",
            geom, 50.0, 1.0,  # Car: 50km, 1h
            geom, 52.0, 1.2   # Bike: 52km, 1.2h
        )
        
        self.assertEqual(comparison['faster_vehicle'], 'car')
        self.assertAlmostEqual(comparison['diff_km'], 2.0, places=1)
        self.assertAlmostEqual(comparison['diff_min'], 12.0, places=1)
        
        # Cleanup
        if os.path.exists("route_comparison.html"):
            os.remove("route_comparison.html")
    
    def test_17_comparison_bike_faster(self):
        """TC17: So sánh - Xe máy nhanh hơn"""
        geom = [[106.6297, 10.8231], [106.7000, 10.9000]]
        
        _, comparison = create_comparison_map(
            10.8231, 106.6297, 10.9000, 106.7000,
            "Start", "End",
            geom, 55.0, 1.5,  # Car: 55km, 1.5h
            geom, 52.0, 1.2   # Bike: 52km, 1.2h
        )
        
        self.assertEqual(comparison['faster_vehicle'], 'bike')
        
        # Cleanup
        if os.path.exists("route_comparison.html"):
            os.remove("route_comparison.html")


class TestUI(unittest.TestCase):
    """Test cases cho module ui.py"""
    
    @patch('builtins.input', return_value='1')
    def test_18_get_vehicle_choice_driving(self, mock_input):
        """TC18: Chọn phương tiện - Ô tô"""
        choice = get_vehicle_choice()
        self.assertEqual(choice, "driving")
    
    @patch('builtins.input', return_value='2')
    def test_19_get_vehicle_choice_bike(self, mock_input):
        """TC19: Chọn phương tiện - Xe máy"""
        choice = get_vehicle_choice()
        self.assertEqual(choice, "bike")
    
    @patch('builtins.input', return_value='3')
    def test_20_get_vehicle_choice_both(self, mock_input):
        """TC20: Chọn phương tiện - So sánh cả hai"""
        choice = get_vehicle_choice()
        self.assertEqual(choice, "both")


def run_tests():
    """Chạy tất cả test cases và tạo báo cáo"""
    # Tạo test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Thêm tất cả test cases
    suite.addTests(loader.loadTestsFromTestCase(TestConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestGeocoding))
    suite.addTests(loader.loadTestsFromTestCase(TestRouting))
    suite.addTests(loader.loadTestsFromTestCase(TestWeather))
    suite.addTests(loader.loadTestsFromTestCase(TestMapping))
    suite.addTests(loader.loadTestsFromTestCase(TestUI))
    
    # Chạy tests với verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # In báo cáo tổng kết
    print("\n" + "="*70)
    print("📊 BÁO CÁO TỔNG KẾT TEST")
    print("="*70)
    print(f"✅ Số test cases chạy: {result.testsRun}")
    print(f"✅ Số test thành công: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Số test thất bại: {len(result.failures)}")
    print(f"⚠️  Số test lỗi: {len(result.errors)}")
    print(f"📈 Tỷ lệ thành công: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("="*70)
    
    return result


if __name__ == "__main__":
    print("="*70)
    print("🧪 CHƯƠNG TRÌNH TEST - TÌM ĐƯỜNG ĐI NGẮN NHẤT")
    print("="*70)
    print("📝 Tổng cộng: 20 test cases")
    print("📦 Bao phủ: config, geocoding, routing, weather, mapping, ui")
    print("="*70)
    print()
    
    result = run_tests()
    
    # Exit code: 0 nếu tất cả pass, 1 nếu có lỗi
    sys.exit(0 if result.wasSuccessful() else 1)
