# Manual Test Cases - Authentication & User Management
# Hướng dẫn test thủ công cho hệ thống xác thực người dùng

## 🎯 Mục đích
Test thủ công các chức năng đăng ký, đăng nhập, và quản lý người dùng

## 📋 Chuẩn bị
- Đảm bảo Supabase đã được cấu hình (file .env)
- Database tables đã được tạo
- File `db_utils.py` tồn tại

---

## TEST CASE 1: Đăng ký tài khoản hợp lệ

### Input:
```python
import db_utils

email = "testuser@example.com"
password = "SecurePassword123!"

success, result = db_utils.add_user(email, password)

print(f"Đăng ký thành công: {success}")
if success:
    print(f"User ID: {result}")
else:
    print(f"Lỗi: {result}")
```

### Expected Output:
```
Đăng ký thành công: True
User ID: <số nguyên, ví dụ: 1, 2, 3...>

Kiểm tra trong database:
✅ User mới được tạo
✅ Email đúng
✅ Password đã được hash (không lưu plain text)
✅ Có created_at timestamp
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 2: Đăng ký với email đã tồn tại

### Input:
```python
import db_utils

# Đăng ký lần 1
email = "duplicate@example.com"
password = "Password123"

success1, result1 = db_utils.add_user(email, password)
print(f"Lần 1 - Success: {success1}, Result: {result1}")

# Đăng ký lần 2 với cùng email
success2, result2 = db_utils.add_user(email, password)
print(f"Lần 2 - Success: {success2}, Message: {result2}")
```

### Expected Output:
```
Lần 1 - Success: True, Result: <user_id>
Lần 2 - Success: False, Message: Email already registered

Lần 2 phải thất bại với thông báo email đã tồn tại
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 3: Đăng nhập với thông tin hợp lệ

### Input:
```python
import db_utils

# Đăng ký user trước
email = "validuser@example.com"
password = "MyPassword123"

db_utils.add_user(email, password)

# Đăng nhập
success, user_id = db_utils.verify_user(email, password)

print(f"Đăng nhập thành công: {success}")
if success:
    print(f"User ID: {user_id}")
```

### Expected Output:
```
Đăng nhập thành công: True
User ID: <số nguyên>

Verify thành công và trả về đúng user_id
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 4: Đăng nhập với mật khẩu sai

### Input:
```python
import db_utils

# Đăng ký user
email = "user@example.com"
correct_password = "CorrectPassword123"
wrong_password = "WrongPassword456"

db_utils.add_user(email, correct_password)

# Thử đăng nhập với mật khẩu sai
success, result = db_utils.verify_user(email, wrong_password)

print(f"Đăng nhập thành công: {success}")
print(f"Result: {result}")
```

### Expected Output:
```
Đăng nhập thành công: False
Result: False (hoặc None)

Đăng nhập phải thất bại khi password sai
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 5: Đăng nhập với email không tồn tại

### Input:
```python
import db_utils

email = "nonexistent@example.com"
password = "AnyPassword123"

success, result = db_utils.verify_user(email, password)

print(f"Đăng nhập thành công: {success}")
print(f"Result: {result}")
```

### Expected Output:
```
Đăng nhập thành công: False
Result: False (hoặc None)

Không thể đăng nhập với email không tồn tại
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 6: Lấy thông tin user tồn tại

### Input:
```python
import db_utils

# Đăng ký user
email = "getuser@example.com"
password = "Password123"

success, user_id = db_utils.add_user(email, password)

# Lấy thông tin user
user = db_utils.get_user(email)

print(f"User found: {user is not None}")
if user:
    print(f"ID: {user.get('id')}")
    print(f"Email: {user.get('email')}")
    print(f"Has password: {'password' in user}")
    print(f"Password is hashed: {user.get('password') != password}")
```

### Expected Output:
```
User found: True
ID: <số nguyên>
Email: getuser@example.com
Has password: True
Password is hashed: True

User được tìm thấy với đầy đủ thông tin
Password đã được hash (không phải plain text)
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 7: Lấy thông tin user không tồn tại

### Input:
```python
import db_utils

email = "notfound@example.com"

user = db_utils.get_user(email)

print(f"User found: {user is not None}")
print(f"User: {user}")
```

### Expected Output:
```
User found: False
User: None

Trả về None khi user không tồn tại
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 8: Password được hash đúng cách

### Input:
```python
import db_utils
import bcrypt

email = "hashtest@example.com"
original_password = "MySecretPassword123"

# Đăng ký user
success, user_id = db_utils.add_user(email, original_password)

# Lấy user từ DB
user = db_utils.get_user(email)

hashed_password = user['password']

print(f"Original password: {original_password}")
print(f"Hashed password: {hashed_password}")
print(f"Passwords match: {original_password == hashed_password}")
print(f"Is bcrypt hash: {hashed_password.startswith('$2b$')}")

# Verify hash
is_valid = bcrypt.checkpw(
    original_password.encode('utf-8'),
    hashed_password.encode('utf-8')
)
print(f"Hash verification: {is_valid}")
```

### Expected Output:
```
Original password: MySecretPassword123
Hashed password: $2b$12$xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
Passwords match: False
Is bcrypt hash: True
Hash verification: True

✅ Password được hash, không lưu plain text
✅ Hash bắt đầu với $2b$ (bcrypt)
✅ Hash có thể verify với password gốc
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 9: Bcrypt tạo salt khác nhau mỗi lần

### Input:
```python
import bcrypt

password = "SamePassword123"

# Hash 2 lần với cùng password
hash1 = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
hash2 = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

print(f"Hash 1: {hash1}")
print(f"Hash 2: {hash2}")
print(f"Hashes are different: {hash1 != hash2}")

# Nhưng cả 2 đều verify được
verify1 = bcrypt.checkpw(password.encode('utf-8'), hash1.encode('utf-8'))
verify2 = bcrypt.checkpw(password.encode('utf-8'), hash2.encode('utf-8'))

print(f"Hash 1 verifies: {verify1}")
print(f"Hash 2 verifies: {verify2}")
```

### Expected Output:
```
Hash 1: $2b$12$aaaaaaaaaaaaaaaaaaaaaa...
Hash 2: $2b$12$bbbbbbbbbbbbbbbbbbbbbb...
Hashes are different: True
Hash 1 verifies: True
Hash 2 verifies: True

✅ Mỗi lần hash tạo ra salt khác nhau
✅ Cả 2 hash đều verify được với password gốc
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 10: Đăng ký với email có ký tự đặc biệt

### Input:
```python
import db_utils

special_emails = [
    "user+tag@example.com",
    "user.name@example.co.uk",
    "user_123@example-domain.com"
]

for email in special_emails:
    success, result = db_utils.add_user(email, "Password123")
    print(f"{email}: {success}")
```

### Expected Output:
```
user+tag@example.com: True
user.name@example.co.uk: True
user_123@example-domain.com: True

✅ Email với ký tự đặc biệt hợp lệ được chấp nhận
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 11: Đăng ký với mật khẩu rất dài

### Input:
```python
import db_utils

email = "longpass@example.com"
long_password = "a" * 200  # 200 ký tự

success, result = db_utils.add_user(email, long_password)

print(f"Success: {success}")
if success:
    # Verify lại
    verify_success, user_id = db_utils.verify_user(email, long_password)
    print(f"Verify success: {verify_success}")
```

### Expected Output:
```
Success: True
Verify success: True

✅ Password dài được xử lý đúng
✅ Có thể verify lại với password dài
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 12: Đăng ký với mật khẩu có Unicode

### Input:
```python
import db_utils

email = "unicode@example.com"
unicode_password = "Mật_Khẩu_Việt_Nam_123_🔒"

success, result = db_utils.add_user(email, unicode_password)

print(f"Success: {success}")
if success:
    # Verify lại
    verify_success, user_id = db_utils.verify_user(email, unicode_password)
    print(f"Verify success: {verify_success}")
```

### Expected Output:
```
Success: True
Verify success: True

✅ Password Unicode được xử lý đúng
✅ Có thể verify lại với password Unicode
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 13: Đăng nhập với thông tin rỗng

### Input:
```python
import db_utils

test_cases = [
    ("", ""),
    ("", "password"),
    ("email@example.com", "")
]

for email, password in test_cases:
    success, result = db_utils.verify_user(email, password)
    print(f"Email: '{email}', Password: '{password}' -> Success: {success}")
```

### Expected Output:
```
Email: '', Password: '' -> Success: False
Email: '', Password: 'password' -> Success: False
Email: 'email@example.com', Password: '' -> Success: False

✅ Tất cả các trường hợp rỗng đều fail
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 14: SQL Injection prevention

### Input:
```python
import db_utils

malicious_inputs = [
    "admin'--",
    "admin' OR '1'='1",
    "'; DROP TABLE users; --",
    "admin' AND 1=1--"
]

for malicious_email in malicious_inputs:
    success, result = db_utils.verify_user(malicious_email, "password")
    print(f"Email: {malicious_email}")
    print(f"  Success: {success}")
    print(f"  Result: {result}")
```

### Expected Output:
```
Email: admin'--
  Success: False
  Result: False

Email: admin' OR '1'='1
  Success: False
  Result: False

...

✅ Tất cả SQL injection attempts đều fail
✅ Không có lỗi database
✅ Không có user nào được trả về
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 15: User ID consistency

### Input:
```python
import db_utils

email = "consistency@example.com"
password = "Password123"

# Đăng ký
success, user_id = db_utils.add_user(email, password)
print(f"Registered - User ID: {user_id}")

# Lấy user nhiều lần
user1 = db_utils.get_user(email)
user2 = db_utils.get_user(email)
user3 = db_utils.get_user(email)

print(f"Get 1 - User ID: {user1['id']}")
print(f"Get 2 - User ID: {user2['id']}")
print(f"Get 3 - User ID: {user3['id']}")

print(f"All IDs match: {user1['id'] == user2['id'] == user3['id'] == user_id}")
```

### Expected Output:
```
Registered - User ID: 123
Get 1 - User ID: 123
Get 2 - User ID: 123
Get 3 - User ID: 123
All IDs match: True

✅ User ID nhất quán qua nhiều lần query
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 16: Verify trả về đúng user_id

### Input:
```python
import db_utils

email = "verifyid@example.com"
password = "Password123"

# Đăng ký và lấy ID
success, registered_id = db_utils.add_user(email, password)
print(f"Registered ID: {registered_id}")

# Verify và lấy ID
verify_success, verified_id = db_utils.verify_user(email, password)
print(f"Verified ID: {verified_id}")

# Lấy user và kiểm tra ID
user = db_utils.get_user(email)
print(f"User ID from get_user: {user['id']}")

print(f"All IDs match: {registered_id == verified_id == user['id']}")
```

### Expected Output:
```
Registered ID: 456
Verified ID: 456
User ID from get_user: 456
All IDs match: True

✅ verify_user trả về đúng user_id
✅ ID nhất quán giữa các functions
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 17: Cấu trúc dữ liệu user đầy đủ

### Input:
```python
import db_utils

email = "structure@example.com"
password = "Password123"

db_utils.add_user(email, password)
user = db_utils.get_user(email)

required_fields = ['id', 'email', 'password']

print("User data structure:")
for field in required_fields:
    has_field = field in user
    print(f"  {field}: {has_field}")
    if has_field:
        value = user[field]
        print(f"    Value type: {type(value).__name__}")
        if field == 'password':
            print(f"    Is hashed: {not value.startswith('Password')}")
```

### Expected Output:
```
User data structure:
  id: True
    Value type: int (hoặc str)
  email: True
    Value type: str
  password: True
    Value type: str
    Is hashed: True

✅ User có đầy đủ các trường bắt buộc
✅ Kiểu dữ liệu đúng
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 18: Timestamp created_at

### Input:
```python
import db_utils
from datetime import datetime

email = "timestamp@example.com"
password = "Password123"

before = datetime.utcnow()
success, user_id = db_utils.add_user(email, password)
after = datetime.utcnow()

user = db_utils.get_user(email)

print(f"User created: {success}")
if 'created_at' in user:
    created_at = user['created_at']
    print(f"created_at: {created_at}")
    print(f"created_at type: {type(created_at).__name__}")
    
    # Parse nếu là string
    if isinstance(created_at, str):
        created_dt = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        print(f"Created between valid time range: {before <= created_dt <= after}")
else:
    print("created_at field missing")
```

### Expected Output:
```
User created: True
created_at: 2025-11-30T10:30:45.123456
created_at type: str (hoặc datetime)
Created between valid time range: True

✅ Có trường created_at
✅ Timestamp hợp lý (trong khoảng thời gian test)
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 19: Database không được cấu hình

### Input:
```python
import db_utils
import os

# Backup current config
original_supabase = db_utils.supabase

# Set to None to simulate no config
db_utils.supabase = None

success, message = db_utils.add_user("test@example.com", "password")

print(f"Success: {success}")
print(f"Message: {message}")

# Restore
db_utils.supabase = original_supabase
```

### Expected Output:
```
Success: False
Message: Supabase not configured (hoặc tương tự)

✅ Xử lý gracefully khi DB không được cấu hình
✅ Trả về thông báo lỗi rõ ràng
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 20: Test tích hợp flow hoàn chỉnh

### Input:
```python
import db_utils

print("=" * 60)
print("COMPLETE USER AUTHENTICATION FLOW TEST")
print("=" * 60)

# Step 1: Đăng ký user mới
print("\n1. REGISTRATION")
email = "complete.test@example.com"
password = "SecurePass123!"

success, user_id = db_utils.add_user(email, password)
print(f"   ✓ Registration: {'SUCCESS' if success else 'FAILED'}")
print(f"   ✓ User ID: {user_id}")

# Step 2: Lấy thông tin user
print("\n2. GET USER INFO")
user = db_utils.get_user(email)
print(f"   ✓ User found: {user is not None}")
if user:
    print(f"   ✓ Email: {user['email']}")
    print(f"   ✓ ID matches: {user['id'] == user_id}")
    print(f"   ✓ Password hashed: {user['password'] != password}")

# Step 3: Đăng nhập với thông tin đúng
print("\n3. LOGIN - CORRECT PASSWORD")
success, verified_id = db_utils.verify_user(email, password)
print(f"   ✓ Login: {'SUCCESS' if success else 'FAILED'}")
print(f"   ✓ ID matches: {verified_id == user_id}")

# Step 4: Đăng nhập với mật khẩu sai
print("\n4. LOGIN - WRONG PASSWORD")
success, result = db_utils.verify_user(email, "WrongPassword")
print(f"   ✓ Login failed as expected: {not success}")

# Step 5: Thử đăng ký lại cùng email
print("\n5. DUPLICATE REGISTRATION")
success, message = db_utils.add_user(email, "NewPassword")
print(f"   ✓ Duplicate prevented: {not success}")
print(f"   ✓ Error message: {message}")

# Step 6: Verify password vẫn là password cũ
print("\n6. PASSWORD UNCHANGED")
success, verified_id = db_utils.verify_user(email, password)
print(f"   ✓ Original password still works: {success}")

print("\n" + "=" * 60)
print("TEST COMPLETED")
print("=" * 60)
```

### Expected Output:
```
============================================================
COMPLETE USER AUTHENTICATION FLOW TEST
============================================================

1. REGISTRATION
   ✓ Registration: SUCCESS
   ✓ User ID: <số nguyên>

2. GET USER INFO
   ✓ User found: True
   ✓ Email: complete.test@example.com
   ✓ ID matches: True
   ✓ Password hashed: True

3. LOGIN - CORRECT PASSWORD
   ✓ Login: SUCCESS
   ✓ ID matches: True

4. LOGIN - WRONG PASSWORD
   ✓ Login failed as expected: True

5. DUPLICATE REGISTRATION
   ✓ Duplicate prevented: True
   ✓ Error message: Email already registered

6. PASSWORD UNCHANGED
   ✓ Original password still works: True

============================================================
TEST COMPLETED
============================================================

Tất cả các bước phải PASS:
✅ Đăng ký thành công
✅ Lấy thông tin user đúng
✅ Đăng nhập với password đúng thành công
✅ Đăng nhập với password sai thất bại
✅ Không thể đăng ký duplicate email
✅ Password không bị thay đổi
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output:
_______________________________________________
_______________________________________________
_______________________________________________
```

---

## 📝 Tổng kết Test

### Thống kê
- **Tổng số test cases**: 20
- **Passed**: _____ / 20
- **Failed**: _____ / 20
- **Success Rate**: _____ %

### Phân loại lỗi (nếu có)
- [ ] Đăng ký không hoạt động
- [ ] Đăng nhập thất bại
- [ ] Password không được hash
- [ ] SQL injection không được prevent
- [ ] Duplicate email không được chặn
- [ ] User data structure thiếu fields
- [ ] Khác: _________________

### Ghi chú
```
_________________________________________________
_________________________________________________
_________________________________________________
```

---

## 🔧 Hướng dẫn sử dụng

1. **Chuẩn bị môi trường**:
   ```powershell
   # Đảm bảo có .env với Supabase credentials
   # SUPABASE_URL=https://xxx.supabase.co
   # SUPABASE_KEY=eyJxxx...
   ```

2. **Chạy test**:
   - Mở Python terminal
   - Copy từng test case
   - Execute và quan sát output

3. **Kiểm tra database**:
   - Vào Supabase Dashboard
   - Xem table `users`
   - Verify dữ liệu được lưu đúng

4. **Clean up** (sau khi test):
   ```python
   # Xóa test users nếu cần
   # (thực hiện qua Supabase dashboard hoặc SQL)
   ```

### Tips
- Test theo thứ tự từ trên xuống
- Mỗi test tạo email khác nhau để tránh conflict
- Lưu output để so sánh
- Nếu test FAIL, kiểm tra:
  - Supabase connection
  - Table structure
  - Permissions trong Supabase

### Security Checklist
- ✅ Password được hash (bcrypt)
- ✅ Không lưu plain text password
- ✅ SQL injection được prevent
- ✅ Duplicate email được chặn
- ✅ Empty input được validate
