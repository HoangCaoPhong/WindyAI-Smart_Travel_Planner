# Test Suite - Smart Travel Project

## Tổng quan
Test suite toàn diện với **20 test cases** bao phủ tất cả các trường hợp cho thuật toán AI lập kế hoạch du lịch.

## Cấu trúc Test Cases

### 1. Geo Utils Tests (TC01-03)
- **TC01**: Kiểm tra khoảng cách giữa cùng một vị trí (phải = 0)
- **TC02**: Xác thực tính toán khoảng cách với giá trị đã biết
- **TC03**: Tính toán thông tin di chuyển cho tất cả các phương tiện (đi bộ, xe máy, taxi)

### 2. Scorer Tests (TC04-07)
- **TC04**: Khớp hoàn hảo với sở thích người dùng (score = 1.0)
- **TC05**: Không khớp sở thích (score = 0.0)
- **TC06**: Khớp một phần sở thích
- **TC07**: So sánh điểm số giữa các POI (điểm thấp hơn = tốt hơn)

### 3. POI Loading Tests (TC08-10)
- **TC08**: Load POIs từ CSV hợp lệ
- **TC09**: Xử lý POIs với tags rỗng
- **TC10**: Chuyển đổi kiểu dữ liệu chính xác

### 4. Route Planning Tests (TC11-17)
- **TC11**: Lập kế hoạch tuyến đường cơ bản
- **TC12**: Ràng buộc ngân sách chặt chẽ
- **TC13**: Ràng buộc thời gian chặt chẽ
- **TC14**: Tôn trọng giờ mở cửa của POI
- **TC15**: Xử lý danh sách POI trống
- **TC16**: Xử lý trường hợp không có POI khả thi
- **TC17**: Ưu tiên POI theo sở thích

### 5. Optimizer Tests (TC18-19)
- **TC18**: 2-opt cải thiện hoặc duy trì chất lượng tuyến đường
- **TC19**: 2-opt với tuyến đường quá ngắn để tối ưu

### 6. Integration Test (TC20)
- **TC20**: Quy trình đầy đủ từ CSV đến tuyến đường tối ưu
  - Kiểm tra tất cả ràng buộc (ngân sách, thời gian, giờ mở cửa)
  - Kiểm tra tính liên tục của tuyến đường
  - Không trùng lặp điểm tham quan

## Cài đặt

```bash
# Cài đặt dependencies
pip install -r requirements.txt
```

## Chạy Tests

### Chạy tất cả tests
```bash
pytest tests/test_comprehensive.py -v
```

### Chạy tests với coverage
```bash
pytest tests/test_comprehensive.py --cov=core --cov-report=html -v
```

### Chạy một test cụ thể
```bash
pytest tests/test_comprehensive.py::TestRoutePlanning::test_11_plan_route_basic -v
```

### Chạy một nhóm test
```bash
pytest tests/test_comprehensive.py::TestGeoUtils -v
```

## Kết quả mong đợi

Tất cả 20 test cases sẽ pass nếu:
- ✅ Hàm tính toán địa lý hoạt động chính xác
- ✅ Hệ thống đánh giá POI hoạt động đúng
- ✅ Load và parse dữ liệu CSV chính xác
- ✅ Thuật toán lập kế hoạch tôn trọng tất cả ràng buộc
- ✅ Tối ưu hóa tuyến đường cải thiện chất lượng
- ✅ Tích hợp end-to-end hoạt động trơn tru

## Coverage mục tiêu

- **core/utils_geo.py**: 100%
- **core/scorer.py**: 100%
- **core/solver_route.py**: ≥ 95%
- **core/optimizer.py**: ≥ 90%
- **Overall**: ≥ 90%

## Báo cáo lỗi

Nếu test fail, kiểm tra:
1. Dữ liệu test CSV được tạo đúng trong `tests/test_data/`
2. Các hằng số trong `core/config.py` phù hợp
3. Logic thuật toán trong `core/solver_route.py`
4. Hàm tối ưu trong `core/optimizer.py`

## Test Data

Test data được tạo tự động trong thư mục `tests/test_data/` và sẽ được dọn dẹp sau khi chạy tests.
