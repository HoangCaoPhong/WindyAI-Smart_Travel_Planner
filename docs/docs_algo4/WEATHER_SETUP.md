# Hướng Dẫn Cấu Hình Thời Tiết

## Bước 1: Đăng Ký API Key Miễn Phí

1. Truy cập: https://openweathermap.org/api
2. Click "Sign Up" (góc trên bên phải)
3. Điền thông tin:
   - Username
   - Email
   - Password
   - Chọn "I am not a robot"
4. Xác nhận email
5. Sau khi đăng nhập, vào "API keys" tab
6. Copy "Default" API key (hoặc tạo key mới)

## Bước 2: Thêm API Key Vào Code

Mở file `test.py` và tìm dòng:

```python
OPENWEATHER_API_KEY = "YOUR_API_KEY_HERE"
```

Thay `YOUR_API_KEY_HERE` bằng API key của bạn:

```python
OPENWEATHER_API_KEY = "abc123def456..."  # Thay bằng key thật
```

## Bước 3: Chạy Chương Trình

Khi chạy, chương trình sẽ tự động hiển thị thông tin thời tiết cho:
- Điểm bắt đầu
- Điểm đến

### Thông Tin Hiển Thị:
- 🌡️ Nhiệt độ hiện tại và cảm giác như
- ☁️ Tình trạng thời tiết (mây, nắng, mưa...)
- 💧 Độ ẩm không khí
- 💨 Tốc độ gió

### Ví Dụ Output:

```
  🌤️  Thời tiết tại điểm đầu:
     🌡️  Nhiệt độ: 28.5°C (cảm giác như 31.2°C)
     ☁️  Tình trạng: Mây rải rác
     💧 Độ ẩm: 75%
     💨 Gió: 3.2 m/s
```

## Lưu Ý:

- **Free Plan**: 1,000 calls/ngày, 60 calls/phút
- API key có thể mất 10-15 phút để active sau khi tạo
- Nếu không muốn dùng thời tiết, cứ để `YOUR_API_KEY_HERE` — chương trình sẽ bỏ qua và chỉ hiển thị cảnh báo nhẹ

## Troubleshooting:

**Lỗi 401 (Unauthorized):**
- API key chưa active → đợi 15 phút
- API key sai → kiểm tra lại

**Lỗi 429 (Too Many Requests):**
- Vượt giới hạn miễn phí → đợi 1 phút hoặc nâng cấp plan

**Không hiển thị thời tiết:**
- Kiểm tra kết nối internet
- Xem có lỗi nào in ra không
