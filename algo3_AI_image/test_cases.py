# test_cases.py
"""
Test cases toàn diện cho hệ thống nhận diện địa điểm du lịch Việt Nam
20 test cases bao phủ tất cả các trường hợp
"""

import unittest
import torch
import os
import sys
from PIL import Image
import io
import numpy as np
from torchvision import transforms

# Import các hàm cần test
from predict_vn import (
    predict_image_path, 
    predict_pil_image, 
    predict_image_bytes,
    CLASS_NAMES,
    model,
    preprocess,
    device
)


class TestVietnameseLocationRecognition(unittest.TestCase):
    """Test suite cho hệ thống nhận diện địa điểm du lịch"""
    
    @classmethod
    def setUpClass(cls):
        """Khởi tạo một lần cho tất cả test cases"""
        cls.test_image_dir = "data/val"
        cls.expected_classes = 21  # Số lớp trong dự án
        cls.confidence_threshold = 0.0  # Ngưỡng tin cậy tối thiểu
        
    def create_dummy_image(self, size=(224, 224), mode="RGB"):
        """Tạo ảnh giả để test"""
        return Image.new(mode, size, color=(128, 128, 128))
    
    def create_random_image(self, size=(224, 224)):
        """Tạo ảnh random để test"""
        arr = np.random.randint(0, 255, (size[0], size[1], 3), dtype=np.uint8)
        return Image.fromarray(arr)
    
    # ========================================
    # TEST 1-5: Kiểm tra cấu hình và khởi tạo model
    # ========================================
    
    def test_01_model_loaded_successfully(self):
        """Test 1: Model được load thành công"""
        self.assertIsNotNone(model)
        self.assertTrue(isinstance(model, torch.nn.Module))
        
    def test_02_correct_number_of_classes(self):
        """Test 2: Số lượng lớp đúng (21 địa điểm)"""
        self.assertEqual(len(CLASS_NAMES), self.expected_classes)
        
    def test_03_model_in_eval_mode(self):
        """Test 3: Model ở chế độ evaluation"""
        self.assertFalse(model.training)
        
    def test_04_device_configuration(self):
        """Test 4: Device được cấu hình đúng"""
        self.assertIn(str(device), ['cpu', 'cuda'])
        
    def test_05_all_classes_exist(self):
        """Test 5: Tất cả 21 địa điểm có trong danh sách"""
        expected_locations = [
            "Bitexco", "Bưu điện thành phố", "Bảo tàng Chứng tích Chiến tranh",
            "Bảo tàng lịch sử tpHCM", "Bảo tàng mỹ thuật tpHCM", "Bến Bạch Đằng",
            "Bến Nhà Rồng", "Chợ Bến Thành", "Công viên 30 tháng 4", "Cầu Ánh Sao",
            "Dinh Độc Lập", "Ga Sài Gòn", "Landmark 81", "Nhà hát Thành phố",
            "Nhà thờ Đức Bà", "Phố đi bộ Nguyễn Huệ", "SaiGon Center", "Suối Tiên",
            "Thảo cầm viên", "UBND _tp Hồ Chí Minh", "Đường sách Nguyễn Văn Bình"
        ]
        for location in expected_locations:
            self.assertIn(location, CLASS_NAMES)
    
    # ========================================
    # TEST 6-10: Kiểm tra hàm dự đoán từ đường dẫn
    # ========================================
    
    def test_06_predict_from_valid_path(self):
        """Test 6: Dự đoán từ đường dẫn file hợp lệ"""
        # Tìm ảnh đầu tiên trong thư mục validation
        for class_name in os.listdir(self.test_image_dir):
            class_path = os.path.join(self.test_image_dir, class_name)
            if os.path.isdir(class_path):
                images = [f for f in os.listdir(class_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
                if images:
                    test_image_path = os.path.join(class_path, images[0])
                    label, confidence = predict_image_path(test_image_path)
                    
                    self.assertIsInstance(label, str)
                    self.assertIsInstance(confidence, float)
                    self.assertGreaterEqual(confidence, 0.0)
                    self.assertLessEqual(confidence, 1.0)
                    self.assertIn(label, CLASS_NAMES)
                    break
    
    def test_07_predict_invalid_path_raises_error(self):
        """Test 7: Dự đoán từ đường dẫn không tồn tại báo lỗi"""
        with self.assertRaises(FileNotFoundError):
            predict_image_path("nonexistent_image.jpg")
    
    def test_08_predict_from_different_image_formats(self):
        """Test 8: Dự đoán với nhiều định dạng ảnh (JPG, PNG)"""
        test_formats = ['.jpg', '.jpeg', '.png']
        for class_name in os.listdir(self.test_image_dir):
            class_path = os.path.join(self.test_image_dir, class_name)
            if os.path.isdir(class_path):
                for ext in test_formats:
                    images = [f for f in os.listdir(class_path) if f.lower().endswith(ext)]
                    if images:
                        test_image_path = os.path.join(class_path, images[0])
                        label, confidence = predict_image_path(test_image_path)
                        self.assertIsNotNone(label)
                        self.assertIsNotNone(confidence)
                        return
    
    def test_09_predict_confidence_in_valid_range(self):
        """Test 9: Độ tin cậy nằm trong khoảng [0, 1]"""
        img = self.create_random_image()
        label, confidence = predict_pil_image(img)
        
        self.assertGreaterEqual(confidence, 0.0)
        self.assertLessEqual(confidence, 1.0)
    
    def test_10_predict_returns_valid_class(self):
        """Test 10: Kết quả dự đoán luôn nằm trong danh sách lớp"""
        img = self.create_random_image()
        label, confidence = predict_pil_image(img)
        
        self.assertIn(label, CLASS_NAMES)
    
    # ========================================
    # TEST 11-15: Kiểm tra hàm dự đoán từ PIL Image
    # ========================================
    
    def test_11_predict_from_pil_rgb_image(self):
        """Test 11: Dự đoán từ PIL Image RGB"""
        img = self.create_dummy_image(mode="RGB")
        label, confidence = predict_pil_image(img)
        
        self.assertIsInstance(label, str)
        self.assertIsInstance(confidence, float)
    
    def test_12_predict_from_pil_grayscale_image(self):
        """Test 12: Dự đoán từ ảnh grayscale (tự động convert RGB)"""
        img = self.create_dummy_image(mode="L")  # Grayscale
        label, confidence = predict_pil_image(img)
        
        self.assertIsNotNone(label)
        self.assertIsNotNone(confidence)
    
    def test_13_predict_from_pil_rgba_image(self):
        """Test 13: Dự đoán từ ảnh RGBA (có alpha channel)"""
        img = self.create_dummy_image(mode="RGBA")
        label, confidence = predict_pil_image(img)
        
        self.assertIsNotNone(label)
        self.assertIsNotNone(confidence)
    
    def test_14_predict_from_different_image_sizes(self):
        """Test 14: Dự đoán từ ảnh có kích thước khác nhau"""
        sizes = [(100, 100), (224, 224), (512, 512), (800, 600), (1920, 1080)]
        
        for size in sizes:
            img = self.create_random_image(size)
            label, confidence = predict_pil_image(img)
            
            self.assertIsNotNone(label, f"Failed for size {size}")
            self.assertIsNotNone(confidence, f"Failed for size {size}")
    
    def test_15_predict_consistent_results(self):
        """Test 15: Cùng ảnh dự đoán nhiều lần cho kết quả nhất quán"""
        img = self.create_random_image()
        
        results = []
        for _ in range(5):
            label, confidence = predict_pil_image(img)
            results.append((label, confidence))
        
        # Kiểm tra tất cả kết quả giống nhau
        first_result = results[0]
        for result in results:
            self.assertEqual(result[0], first_result[0])
            self.assertAlmostEqual(result[1], first_result[1], places=5)
    
    # ========================================
    # TEST 16-20: Kiểm tra hàm dự đoán từ bytes và edge cases
    # ========================================
    
    def test_16_predict_from_image_bytes(self):
        """Test 16: Dự đoán từ image bytes"""
        img = self.create_random_image()
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')
        image_bytes = buffer.getvalue()
        
        label, confidence = predict_image_bytes(image_bytes)
        
        self.assertIsInstance(label, str)
        self.assertIsInstance(confidence, float)
        self.assertIn(label, CLASS_NAMES)
    
    def test_17_predict_from_png_bytes(self):
        """Test 17: Dự đoán từ PNG bytes"""
        img = self.create_random_image()
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        image_bytes = buffer.getvalue()
        
        label, confidence = predict_image_bytes(image_bytes)
        
        self.assertIsNotNone(label)
        self.assertIsNotNone(confidence)
    
    def test_18_predict_invalid_bytes_raises_error(self):
        """Test 18: Bytes không hợp lệ báo lỗi"""
        invalid_bytes = b"This is not an image"
        
        with self.assertRaises(Exception):
            predict_image_bytes(invalid_bytes)
    
    def test_19_preprocess_transform_output_shape(self):
        """Test 19: Transform tạo tensor đúng shape [3, 224, 224]"""
        img = self.create_random_image()
        tensor = preprocess(img)
        
        self.assertEqual(tensor.shape, torch.Size([3, 224, 224]))
        self.assertIsInstance(tensor, torch.Tensor)
    
    def test_20_model_output_distribution(self):
        """Test 20: Output model là phân phối xác suất (tổng ~1.0)"""
        img = self.create_random_image()
        tensor = preprocess(img).unsqueeze(0).to(device)
        
        with torch.no_grad():
            outputs = model(tensor)
            probs = torch.softmax(outputs, dim=1)
            prob_sum = probs.sum().item()
        
        # Tổng xác suất phải gần bằng 1.0
        self.assertAlmostEqual(prob_sum, 1.0, places=5)
        
        # Tất cả xác suất phải >= 0
        self.assertTrue(torch.all(probs >= 0).item())


class TestEdgeCasesAndPerformance(unittest.TestCase):
    """Test các trường hợp đặc biệt và hiệu suất"""
    
    def test_unicode_class_names(self):
        """Test: Xử lý tên lớp tiếng Việt có dấu"""
        vietnamese_names = [name for name in CLASS_NAMES if any(ord(c) > 127 for c in name)]
        self.assertGreater(len(vietnamese_names), 0, "Phải có tên tiếng Việt có dấu")
    
    def test_model_inference_speed(self):
        """Test: Tốc độ inference (phải < 2 giây/ảnh trên CPU)"""
        import time
        
        img = Image.new("RGB", (224, 224), color=(128, 128, 128))
        
        start_time = time.time()
        predict_pil_image(img)
        elapsed_time = time.time() - start_time
        
        self.assertLess(elapsed_time, 2.0, "Inference quá chậm")


def run_all_tests():
    """Chạy tất cả test cases và hiển thị báo cáo"""
    # Tạo test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Thêm tất cả test cases
    suite.addTests(loader.loadTestsFromTestCase(TestVietnameseLocationRecognition))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCasesAndPerformance))
    
    # Chạy tests với verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # In báo cáo tổng kết
    print("\n" + "="*70)
    print("KẾT QUẢ TỔNG KẾT TEST CASES")
    print("="*70)
    print(f"Tổng số test cases: {result.testsRun}")
    print(f"✓ Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"✗ Failed: {len(result.failures)}")
    print(f"✗ Errors: {len(result.errors)}")
    print(f"Tỷ lệ thành công: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.2f}%")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
