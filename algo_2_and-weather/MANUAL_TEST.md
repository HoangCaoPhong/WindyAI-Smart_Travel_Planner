# Test Cases Manual - Kiểm Thử Bằng Tay

## Hướng dẫn kiểm thử
- Chạy chương trình: `python main.py`
- Nhập input theo từng test case
- So sánh output thực tế với output mong đợi

---

## TEST CASE 1: Chọn Ô tô - Địa chỉ mặc định

### Input:
```
Địa chỉ bắt đầu: [Enter - để trống]
Địa chỉ đến: [Enter - để trống]
Lựa chọn: 1
```

### Output mong đợi:
```
✅ Tìm thấy: Ho Chi Minh City, Vietnam
✅ Tìm thấy: Hanoi, Vietnam
🌤️ Thông tin thời tiết tại Ho Chi Minh City, Vietnam
🌤️ Thông tin thời tiết tại Hanoi, Vietnam

CHỈ DẪN CHO Ô TÔ
- Khoảng cách: ~1720 km
- Thời gian: ~1030 phút

Bản đồ đã lưu: route_driving.html
```

---

## TEST CASE 2: Chọn Xe máy - Địa chỉ mặc định

### Input:
```
Địa chỉ bắt đầu: [Enter - để trống]
Địa chỉ đến: [Enter - để trống]
Lựa chọn: 2
```

### Output mong đợi:
```
✅ Tìm thấy: Ho Chi Minh City, Vietnam
✅ Tìm thấy: Hanoi, Vietnam
🌤️ Thông tin thời tiết tại Ho Chi Minh City, Vietnam
🌤️ Thông tin thời tiết tại Hanoi, Vietnam

CHỈ DẪN CHO XE MÁY
- Khoảng cách: ~1735 km
- Thời gian: ~1155 phút

Bản đồ đã lưu: route_bike.html
```

---

## TEST CASE 3: So sánh cả hai - Địa chỉ mặc định

### Input:
```
Địa chỉ bắt đầu: [Enter - để trống]
Địa chỉ đến: [Enter - để trống]
Lựa chọn: 3
```

### Output mong đợi:
```
✅ Tìm thấy: Ho Chi Minh City, Vietnam
✅ Tìm thấy: Hanoi, Vietnam
🌤️ Thông tin thời tiết

CHỈ ĐƯỜNG CHO Ô TÔ
- Khoảng cách: ~1720 km
- Thời gian: ~1030 phút

CHỈ ĐƯỜNG CHO XE MÁY
- Khoảng cách: ~1735 km
- Thời gian: ~1155 phút

Bản đồ đã lưu: route_comparison.html

KẾT QUẢ SO SÁNH:
- Chênh lệch khoảng cách: ~15 km
- Chênh lệch thời gian: ~125 phút
- Phương tiện nhanh hơn: Ô tô
```

---

## TEST CASE 4: Địa chỉ tùy chỉnh trong nước - Ô tô

### Input:
```
Địa chỉ bắt đầu: Da Nang
Địa chỉ đến: Nha Trang
Lựa chọn: 1
```

### Output mong đợi:
```
✅ Tìm thấy: Da Nang, Vietnam
✅ Tìm thấy: Nha Trang, Vietnam
🌤️ Thông tin thời tiết

CHỈ DẪN CHO Ô TÔ
- Khoảng cách: ~530 km
- Thời gian: ~360 phút

Bản đồ đã lưu: route_driving.html
```

---

## TEST CASE 5: Địa chỉ tùy chỉnh ngắn - Xe máy

### Input:
```
Địa chỉ bắt đầu: Ben Thanh Market, Ho Chi Minh
Địa chỉ đến: Cu Chi Tunnels
Lựa chọn: 2
```

### Output mong đợi:
```
✅ Tìm thấy: Ben Thanh Market, Ho Chi Minh City, Vietnam
✅ Tìm thấy: Cu Chi Tunnels, Vietnam
🌤️ Thông tin thời tiết

CHỈ DẪN CHO XE MÁY
- Khoảng cách: ~45 km
- Thời gian: ~60 phút

Bản đồ đã lưu: route_bike.html
```

---

## TEST CASE 6: Địa chỉ chi tiết với đường phố

### Input:
```
Địa chỉ bắt đầu: 227 Nguyen Van Cu, District 5, Ho Chi Minh
Địa chỉ đến: Landmark 81, Ho Chi Minh
Lựa chọn: 1
```

### Output mong đợi:
```
✅ Tìm thấy: 227 Nguyen Van Cu, District 5, Ho Chi Minh City, Vietnam
✅ Tìm thấy: Landmark 81, Ho Chi Minh City, Vietnam
🌤️ Thông tin thời tiết

CHỈ DẪN CHO Ô TÔ
- Khoảng cách: ~8 km
- Thời gian: ~15 phút

Bản đồ đã lưu: route_driving.html
```

---

## TEST CASE 7: Địa chỉ quốc tế

### Input:
```
Địa chỉ bắt đầu: Bangkok, Thailand
Địa chỉ đến: Phnom Penh, Cambodia
Lựa chọn: 3
```

### Output mong đợi:
```
✅ Tìm thấy: Bangkok, Thailand
✅ Tìm thấy: Phnom Penh, Cambodia
🌤️ Thông tin thời tiết

CHỈ ĐƯỜNG CHO Ô TÔ
- Khoảng cách: ~400 km
- Thời gian: ~300 phút

CHỈ ĐƯỜNG CHO XE MÁY
- Khoảng cách: ~405 km
- Thời gian: ~320 phút

Bản đồ đã lưu: route_comparison.html
KẾT QUẢ SO SÁNH
```

---

## TEST CASE 8: Địa chỉ thành phố lớn

### Input:
```
Địa chỉ bắt đầu: Singapore
Địa chỉ đến: Kuala Lumpur, Malaysia
Lựa chọn: 1
```

### Output mong đợi:
```
✅ Tìm thấy: Singapore
✅ Tìm thấy: Kuala Lumpur, Malaysia
🌤️ Thông tin thời tiết

CHỈ DẪN CHO Ô TÔ
- Khoảng cách: ~350 km
- Thời gian: ~250 phút

Bản đồ đã lưu: route_driving.html
```

---

## TEST CASE 9: Lựa chọn không hợp lệ → Nhập lại

### Input:
```
Địa chỉ bắt đầu: [Enter]
Địa chỉ đến: [Enter]
Lựa chọn: 5
[Sau thông báo lỗi]
Lựa chọn: 1
```

### Output mong đợi:
```
✅ Tìm thấy: Ho Chi Minh City, Vietnam
✅ Tìm thấy: Hanoi, Vietnam

⚠️ Lựa chọn không hợp lệ! Vui lòng chọn 1, 2 hoặc 3.
[Menu hiện lại]

CHỈ DẪN CHO Ô TÔ
- Khoảng cách: ~1720 km
Bản đồ đã lưu: route_driving.html
```

---

## TEST CASE 10: Địa chỉ không tồn tại

### Input:
```
Địa chỉ bắt đầu: XYZ123NonExistentPlace456
Địa chỉ đến: Hanoi
Lựa chọn: 1
```

### Output mong đợi:
```
❌ Không tìm thấy địa chỉ: XYZ123NonExistentPlace456
[Chương trình kết thúc hoặc yêu cầu nhập lại]
```

---

## TEST CASE 11: Địa chỉ tiếng Việt có dấu

### Input:
```
Địa chỉ bắt đầu: Hồ Gươm, Hà Nội
Địa chỉ đến: Chợ Bến Thành, Sài Gòn
Lựa chọn: 2
```

### Output mong đợi:
```
✅ Tìm thấy: Hồ Gươm, Hanoi, Vietnam
✅ Tìm thấy: Cho Ben Thanh, Ho Chi Minh City, Vietnam
🌤️ Thông tin thời tiết

CHỈ DẪN CHO XE MÁY
- Khoảng cách: ~1720 km
- Thời gian: ~1150 phút

Bản đồ đã lưu: route_bike.html
```

---

## TEST CASE 12: Đường ngắn trong thành phố

### Input:
```
Địa chỉ bắt đầu: District 1, Ho Chi Minh
Địa chỉ đến: District 3, Ho Chi Minh
Lựa chọn: 1
```

### Output mong đợi:
```
✅ Tìm thấy: District 1, Ho Chi Minh City, Vietnam
✅ Tìm thấy: District 3, Ho Chi Minh City, Vietnam
🌤️ Thông tin thời tiết

CHỈ DẪN CHO Ô TÔ
- Khoảng cách: ~3 km
- Thời gian: ~10 phút

Bản đồ đã lưu: route_driving.html
```

---

## TEST CASE 13: Kiểm tra file HTML được tạo

### Input:
```
Địa chỉ bắt đầu: [Enter]
Địa chỉ đến: [Enter]
Lựa chọn: 1
```

### Kiểm tra sau khi chạy:
```
✅ File tồn tại: route_driving.html
✅ Kích thước file: > 10 KB
✅ Mở file bằng browser: Hiển thị bản đồ với tuyến đường màu xanh
✅ Có 2 markers: xanh lá (Start) và đỏ (End)
```

---

## TEST CASE 14: Kiểm tra file comparison

### Input:
```
Địa chỉ bắt đầu: [Enter]
Địa chỉ đến: [Enter]
Lựa chọn: 3
```

### Kiểm tra sau khi chạy:
```
✅ File tồn tại: route_comparison.html
✅ Mở file: Hiển thị 2 tuyến đường
   - Màu xanh dương: Ô tô
   - Màu đỏ: Xe máy
✅ Có legend (chú thích) góc phải trên
✅ Có 2 markers ở 2 đầu
```

---

## TEST CASE 15: Thông tin thời tiết hiển thị

### Input:
```
Địa chỉ bắt đầu: Hanoi
Địa chỉ đến: Ho Chi Minh
Lựa chọn: 1
```

### Output mong đợi (phần thời tiết):
```
🌤️ Thông tin thời tiết tại Hanoi, Vietnam
   🌡️  Nhiệt độ: XX°C
   🤔 Cảm giác như: XX°C
   💧 Độ ẩm: XX%
   ☁️  Mô tả: clear sky / scattered clouds / ...
   💨 Tốc độ gió: X.X m/s

🌤️ Thông tin thời tiết tại Ho Chi Minh City, Vietnam
   [Tương tự]
```

---

## TEST CASE 16: Chỉ dẫn từng bước

### Input:
```
Địa chỉ bắt đầu: Hanoi
Địa chỉ đến: Hai Phong
Lựa chọn: 1
```

### Output mong đợi (phần chỉ dẫn):
```
📍 CHỈ DẪN CHI TIẾT:

1. Head northeast on ... (500 m)
2. Turn right onto Highway 5 (3.5 km)
3. Continue straight (10 km)
...
X. Arrive at destination

🏁 Đã đến đích!
```

---

## TEST CASE 17: So sánh - Ô tô nhanh hơn

### Input:
```
Địa chỉ bắt đầu: Hanoi
Địa chỉ đến: Ha Long
Lựa chọn: 3
```

### Output mong đợi (phần so sánh):
```
📊 KẾT QUẢ SO SÁNH:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   📏 Chênh lệch khoảng cách: X.X km
   ⏱️  Chênh lệch thời gian: XX phút
   🏆 Phương tiện nhanh hơn: Ô tô 🚗
```

---

## TEST CASE 18: So sánh - Xe máy nhanh hơn

### Input:
```
Địa chỉ bắt đầu: District 1, HCMC
Địa chỉ đến: District 7, HCMC
Lựa chọn: 3
```

### Output mong đợi (phần so sánh):
```
📊 KẾT QUẢ SO SÁNH:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   📏 Chênh lệch khoảng cách: X.X km
   ⏱️  Chênh lệch thời gian: XX phút
   🏆 Phương tiện nhanh hơn: Xe máy 🏍️
```

---

## TEST CASE 19: Khoảng cách rất ngắn (< 1 km)

### Input:
```
Địa chỉ bắt đầu: Notre Dame Cathedral, HCMC
Địa chỉ đến: Saigon Central Post Office
Lựa chọn: 1
```

### Output mong đợi:
```
✅ Tìm thấy: Notre Dame Cathedral, Ho Chi Minh City
✅ Tìm thấy: Saigon Central Post Office, Ho Chi Minh City
🌤️ Thông tin thời tiết

CHỈ DẪN CHO Ô TÔ
- Khoảng cách: ~0.2 km
- Thời gian: ~2 phút

Bản đồ đã lưu: route_driving.html
```

---

## TEST CASE 20: Khoảng cách rất dài (> 2000 km)

### Input:
```
Địa chỉ bắt đầu: Ho Chi Minh, Vietnam
Địa chỉ đến: Beijing, China
Lựa chọn: 1
```

### Output mong đợi:
```
✅ Tìm thấy: Ho Chi Minh City, Vietnam
✅ Tìm thấy: Beijing, China
🌤️ Thông tin thời tiết

CHỈ DẪN CHO Ô TÔ
- Khoảng cách: ~2500 km
- Thời gian: ~1800 phút (30 giờ)

Bản đồ đã lưu: route_driving.html
```

---

## Bảng Tổng Hợp Kết Quả Test

| TC | Mô tả | Input | Kết quả mong đợi | Pass/Fail |
|----|-------|-------|------------------|-----------|
| 1  | Ô tô - Mặc định | Enter/Enter/1 | File route_driving.html | ☐ |
| 2  | Xe máy - Mặc định | Enter/Enter/2 | File route_bike.html | ☐ |
| 3  | So sánh - Mặc định | Enter/Enter/3 | File route_comparison.html | ☐ |
| 4  | Địa chỉ tùy chỉnh | Da Nang/Nha Trang/1 | ~530 km | ☐ |
| 5  | Đường ngắn | Ben Thanh/Cu Chi/2 | ~45 km | ☐ |
| 6  | Địa chỉ chi tiết | Nguyen Van Cu/Landmark 81/1 | ~8 km | ☐ |
| 7  | Quốc tế | Bangkok/Phnom Penh/3 | ~400 km | ☐ |
| 8  | Thành phố lớn | Singapore/KL/1 | ~350 km | ☐ |
| 9  | Input không hợp lệ | 5 → 1 | Thông báo lỗi → Thành công | ☐ |
| 10 | Địa chỉ không tồn tại | XYZ123.../Hanoi/1 | Lỗi không tìm thấy | ☐ |
| 11 | Tiếng Việt có dấu | Hồ Gươm/Chợ BT/2 | Thành công | ☐ |
| 12 | Trong thành phố | D1/D3/1 | ~3 km | ☐ |
| 13 | Check file driving | Enter/Enter/1 | File HTML tồn tại | ☐ |
| 14 | Check file comparison | Enter/Enter/3 | 2 tuyến đường | ☐ |
| 15 | Thời tiết hiển thị | Hanoi/HCMC/1 | Nhiệt độ, độ ẩm, gió | ☐ |
| 16 | Chỉ dẫn chi tiết | Hanoi/Hai Phong/1 | Turn left/right... | ☐ |
| 17 | Ô tô nhanh hơn | Hanoi/Ha Long/3 | Faster: Ô tô | ☐ |
| 18 | Xe máy nhanh hơn | D1/D7/3 | Faster: Xe máy | ☐ |
| 19 | Rất ngắn < 1km | Notre Dame/Post Office/1 | ~0.2 km | ☐ |
| 20 | Rất dài > 2000km | HCMC/Beijing/1 | ~2500 km | ☐ |

---

## Ghi Chú Quan Trọng

### Trước khi test:
- ✅ Đã cài đặt: `pip install folium requests`
- ✅ File config.py có API key OpenWeather hợp lệ (nếu muốn thấy thời tiết)
- ✅ Kết nối internet ổn định

### Trong quá trình test:
- ⏱️ Mỗi lần geocode có delay 1 giây (tránh spam API)
- 🌐 API OSRM và Nominatim phải online
- 📁 File HTML sẽ được ghi đè nếu chạy nhiều lần

### Đánh giá Pass/Fail:
- ✅ **PASS**: Output khớp với mong đợi (±10% cho km và phút)
- ❌ **FAIL**: Lỗi, crash, hoặc output sai hoàn toàn
- ⚠️ **WARNING**: Chạy được nhưng có warning/thiếu thông tin thời tiết

---

**Ngày test:** _______________  
**Người test:** _______________  
**Môi trường:** Windows/Linux/Mac  
**Python version:** _______________
