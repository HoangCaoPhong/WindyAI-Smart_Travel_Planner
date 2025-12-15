# Test Suite cho SmartTravel Project

## Tổng quan

Dự án có 2 bộ test chính, mỗi bộ có **20 test cases** bao phủ tất cả các trường hợp:

### 1. **Test Algo5 Suggester** (`test_algo5_suggester.py`)
Bộ test cho thuật toán gợi ý địa điểm du lịch thông minh

### 2. **Test Authentication** (`test_authentication.py`)
Bộ test cho hệ thống xác thực và quản lý người dùng

---

## Cài đặt

```powershell
# Cài đặt dependencies cho test
pip install -r tests/requirements-test.txt
```

---

## Chạy Test

### Chạy tất cả test cases (40 tests)
```powershell
pytest tests/ -v
```

### Chạy riêng từng bộ test

#### Bộ 1: Algo5 Suggester (20 tests)
```powershell
pytest tests/test_algo5_suggester.py -v
```

#### Bộ 2: Authentication (20 tests)
```powershell
pytest tests/test_authentication.py -v
```

### Chạy test cụ thể
```powershell
# Chạy 1 test class
pytest tests/test_algo5_suggester.py::TestHaversineDistance -v

# Chạy 1 test case cụ thể
pytest tests/test_algo5_suggester.py::TestHaversineDistance::test_tc01_same_location -v
```

### Xem coverage
```powershell
pytest tests/ --cov=core --cov=db_utils --cov-report=html
```

---

## Chi tiết Test Cases

### 📍 Bộ 1: Test Algo5 Suggester (20 tests)

#### **TestHaversineDistance** (4 tests)
- ✅ TC01: Khoảng cách giữa 2 điểm giống nhau
- ✅ TC02: Khoảng cách giữa 2 điểm đã biết
- ✅ TC03: Khoảng cách ngắn trong thành phố
- ✅ TC04: Tọa độ âm (bán cầu nam/tây)

#### **TestSuggestPlacesBasic** (4 tests)
- ✅ TC05: Trường hợp bình thường
- ✅ TC06: Ngân sách = 0
- ✅ TC07: Thời gian rất ngắn
- ✅ TC08: Tất cả POI đóng cửa

#### **TestSuggestPlacesEdgeCases** (4 tests)
- ✅ TC09: K lớn hơn số POI
- ✅ TC10: K = 0
- ✅ TC11: Preferences rỗng
- ✅ TC12: Vị trí rất xa

#### **TestSuggestPlacesScoring** (3 tests)
- ✅ TC13: POI gần hơn có điểm cao hơn
- ✅ TC14: Rating cao được ưu tiên
- ✅ TC15: Preference ảnh hưởng điểm

#### **TestSuggestPlacesTimeConstraints** (3 tests)
- ✅ TC16: Lọc theo giờ mở cửa buổi sáng
- ✅ TC17: Lọc theo giờ mở cửa buổi tối
- ✅ TC18: Constraint về end_time

#### **TestSuggestPlacesBudgetConstraints** (2 tests)
- ✅ TC19: Lọc nghiêm ngặt theo ngân sách
- ✅ TC20: Ngân sách âm

---

### 🔐 Bộ 2: Test Authentication (20 tests)

#### **TestUserRegistration** (7 tests)
- ✅ TC01: Đăng ký hợp lệ
- ✅ TC02: Email trùng lặp
- ✅ TC03: Email rỗng
- ✅ TC04: Mật khẩu rỗng
- ✅ TC05: Email có ký tự đặc biệt
- ✅ TC06: Mật khẩu rất dài
- ✅ TC07: Kiểm tra password hashing

#### **TestUserLogin** (6 tests)
- ✅ TC08: Đăng nhập hợp lệ
- ✅ TC09: Mật khẩu sai
- ✅ TC10: Email không tồn tại
- ✅ TC11: Email case sensitive
- ✅ TC12: Thông tin đăng nhập rỗng
- ✅ TC13: SQL injection attempt

#### **TestGetUser** (3 tests)
- ✅ TC14: Lấy user tồn tại
- ✅ TC15: Lấy user không tồn tại
- ✅ TC16: Email có ký tự đặc biệt

#### **TestDatabaseConnection** (3 tests)
- ✅ TC17: Database không được cấu hình
- ✅ TC18: Lỗi kết nối database
- ✅ TC19: Database timeout

#### **TestPasswordSecurity** (1 test)
- ✅ TC20: Bcrypt hash uniqueness

#### **TestUserDataIntegrity** (2 tests)
- ✅ TC21: Cấu trúc dữ liệu user
- ✅ TC22: Timestamp created_at

#### **TestEdgeCases** (6 tests)
- ✅ TC23: Unicode trong password
- ✅ TC24: Whitespace trong email
- ✅ TC25: Nhiều @ trong email
- ✅ TC26: Giá trị null
- ✅ TC27: Email rất dài
- ✅ TC28: Đăng ký đồng thời

#### **TestSessionManagement** (2 tests)
- ✅ TC29: User ID consistency
- ✅ TC30: Verify trả về đúng user_id

---

## Kết quả mong đợi

```
======================== test session starts ========================
collected 40 items

tests/test_algo5_suggester.py::TestHaversineDistance::test_tc01_same_location PASSED [ 2%]
tests/test_algo5_suggester.py::TestHaversineDistance::test_tc02_known_distance PASSED [ 5%]
...
tests/test_authentication.py::TestSessionManagement::test_tc30_verify_returns_correct_user_id PASSED [100%]

======================== 40 passed in 2.34s =========================
```

---

## Cấu trúc thư mục

```
SmartTravelProject-featureAI-algo5-suggester/
├── tests/
│   ├── __init__.py
│   ├── test_algo5_suggester.py      # 20 test cases cho Algo5
│   ├── test_authentication.py       # 20 test cases cho Auth
│   ├── requirements-test.txt        # Dependencies
│   └── README.md                    # File này
├── core/
│   └── algo5/
│       └── algo5_suggester.py       # Code được test
├── db_utils.py                      # Code được test
└── ...
```

---

## Lưu ý

1. **Mock Database**: Test sử dụng `unittest.mock` để mock Supabase, không cần kết nối DB thật
2. **Pytest Fixtures**: Sử dụng fixtures để tạo dữ liệu test tái sử dụng
3. **Coverage**: Bao phủ các trường hợp:
   - ✅ Happy path (trường hợp bình thường)
   - ✅ Edge cases (trường hợp biên)
   - ✅ Error cases (xử lý lỗi)
   - ✅ Security (bảo mật)
   - ✅ Performance (hiệu năng)

---

## Debug Test

```powershell
# Chạy với output chi tiết
pytest tests/ -vv -s

# Dừng tại test fail đầu tiên
pytest tests/ -x

# Chạy lại test failed
pytest tests/ --lf

# Xem traceback đầy đủ
pytest tests/ --tb=long
```

---

## Tích hợp CI/CD

Thêm vào GitHub Actions (`.github/workflows/test.yml`):

```yaml
name: Run Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: |
          pip install -r requirements.txt
          pip install -r tests/requirements-test.txt
          pytest tests/ -v --cov=core --cov=db_utils
```

---

## Báo lỗi

Nếu phát hiện test case thiếu hoặc lỗi, vui lòng mở issue với thông tin:
- Test case nào bị lỗi
- Expected vs Actual result
- Môi trường (Python version, OS)
