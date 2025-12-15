# Test Cases - Hệ thống Nhận diện Địa điểm Du lịch Việt Nam

## Tổng quan
File `test_cases.py` chứa **20 test cases toàn diện** bao phủ tất cả các trường hợp cho hệ thống nhận diện địa điểm du lịch TP.HCM sử dụng deep learning.

## Danh sách 20 Test Cases

### Nhóm 1: Kiểm tra Cấu hình và Khởi tạo Model (Test 1-5)
1. **test_01_model_loaded_successfully**: Kiểm tra model được load thành công
2. **test_02_correct_number_of_classes**: Kiểm tra số lượng lớp đúng (21 địa điểm)
3. **test_03_model_in_eval_mode**: Kiểm tra model ở chế độ evaluation
4. **test_04_device_configuration**: Kiểm tra device (CPU/GPU) được cấu hình đúng
5. **test_05_all_classes_exist**: Kiểm tra tất cả 21 địa điểm có trong danh sách

### Nhóm 2: Kiểm tra Hàm Dự đoán từ Đường dẫn (Test 6-10)
6. **test_06_predict_from_valid_path**: Dự đoán từ đường dẫn file hợp lệ
7. **test_07_predict_invalid_path_raises_error**: Dự đoán từ đường dẫn không tồn tại báo lỗi
8. **test_08_predict_from_different_image_formats**: Dự đoán với nhiều định dạng (JPG, PNG)
9. **test_09_predict_confidence_in_valid_range**: Độ tin cậy nằm trong khoảng [0, 1]
10. **test_10_predict_returns_valid_class**: Kết quả dự đoán nằm trong danh sách lớp

### Nhóm 3: Kiểm tra Hàm Dự đoán từ PIL Image (Test 11-15)
11. **test_11_predict_from_pil_rgb_image**: Dự đoán từ PIL Image RGB
12. **test_12_predict_from_pil_grayscale_image**: Dự đoán từ ảnh grayscale
13. **test_13_predict_from_pil_rgba_image**: Dự đoán từ ảnh RGBA (có alpha channel)
14. **test_14_predict_from_different_image_sizes**: Dự đoán từ ảnh nhiều kích thước khác nhau
15. **test_15_predict_consistent_results**: Cùng ảnh dự đoán nhiều lần cho kết quả nhất quán

### Nhóm 4: Kiểm tra Hàm Dự đoán từ Bytes và Edge Cases (Test 16-20)
16. **test_16_predict_from_image_bytes**: Dự đoán từ JPEG bytes
17. **test_17_predict_from_png_bytes**: Dự đoán từ PNG bytes
18. **test_18_predict_invalid_bytes_raises_error**: Bytes không hợp lệ báo lỗi
19. **test_19_preprocess_transform_output_shape**: Transform tạo tensor đúng shape [3, 224, 224]
20. **test_20_model_output_distribution**: Output model là phân phối xác suất (tổng ~1.0)

### Bonus Tests: Edge Cases và Performance
- **test_unicode_class_names**: Xử lý tên lớp tiếng Việt có dấu
- **test_model_inference_speed**: Tốc độ inference phải < 2 giây/ảnh

## Cách chạy Test Cases

### 1. Chạy tất cả test cases:
```bash
python test_cases.py
```

### 2. Chạy với unittest:
```bash
python -m unittest test_cases.py -v
```

### 3. Chạy một test case cụ thể:
```bash
python -m unittest test_cases.TestVietnameseLocationRecognition.test_01_model_loaded_successfully
```

### 4. Chạy một nhóm test:
```bash
python -m unittest test_cases.TestVietnameseLocationRecognition -v
```

## Yêu cầu
- Python 3.7+
- PyTorch
- torchvision
- Pillow (PIL)
- numpy

## Cài đặt dependencies:
```bash
pip install torch torchvision pillow numpy
```

## Kết quả mong đợi

Khi chạy test cases, bạn sẽ thấy output như sau:

```
test_01_model_loaded_successfully ... ok
test_02_correct_number_of_classes ... ok
test_03_model_in_eval_mode ... ok
...
test_20_model_output_distribution ... ok

======================================================================
KẾT QUẢ TỔNG KẾT TEST CASES
======================================================================
Tổng số test cases: 22
✓ Passed: 22
✗ Failed: 0
✗ Errors: 0
Tỷ lệ thành công: 100.00%
======================================================================
```

## Độ bao phủ Test Coverage

Test cases bao phủ:
- ✅ **Khởi tạo model**: Load model, classes, device
- ✅ **Các hàm dự đoán**: predict_image_path, predict_pil_image, predict_image_bytes
- ✅ **Định dạng ảnh**: JPG, PNG, RGB, RGBA, Grayscale
- ✅ **Kích thước ảnh**: 100x100, 224x224, 512x512, 1920x1080
- ✅ **Edge cases**: File không tồn tại, bytes không hợp lệ
- ✅ **Validation**: Confidence range, class validity, consistency
- ✅ **Performance**: Inference speed
- ✅ **Unicode**: Tên tiếng Việt có dấu

## 21 Địa điểm được Test

1. Bitexco
2. Bưu điện thành phố
3. Bảo tàng Chứng tích Chiến tranh
4. Bảo tàng lịch sử tpHCM
5. Bảo tàng mỹ thuật tpHCM
6. Bến Bạch Đằng
7. Bến Nhà Rồng
8. Chợ Bến Thành
9. Công viên 30 tháng 4
10. Cầu Ánh Sao
11. Dinh Độc Lập
12. Ga Sài Gòn
13. Landmark 81
14. Nhà hát Thành phố
15. Nhà thờ Đức Bà
16. Phố đi bộ Nguyễn Huệ
17. SaiGon Center
18. Suối Tiên
19. Thảo cầm viên
20. UBND tp Hồ Chí Minh
21. Đường sách Nguyễn Văn Bình

## Troubleshooting

### Lỗi: "Model not found"
Đảm bảo file `model_vietnam.pth` và `classes.txt` tồn tại trong thư mục dự án.

### Lỗi: "Data directory not found"
Đảm bảo thư mục `data/val/` tồn tại với các folder chứa ảnh validation.

### Lỗi: "CUDA out of memory"
Test cases sẽ tự động chuyển sang CPU nếu không có GPU.

## Ghi chú
- Test cases được thiết kế để chạy nhanh và hiệu quả
- Không cần GPU để chạy test (tự động fallback về CPU)
- Test cases có thể được tích hợp vào CI/CD pipeline
