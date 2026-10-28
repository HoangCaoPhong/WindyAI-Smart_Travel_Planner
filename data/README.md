# Dữ Liệu POIs - Hướng Dẫn

## 📊 Tổng Quan

Project có **2 datasets** POI cho TP.HCM:

### 1. `pois_hcm.csv` - Dataset Gốc
- **Số lượng:** 20 POIs
- **Nguồn:** Tạo thủ công
- **Ưu điểm:** Dữ liệu chất lượng cao, đã kiểm tra
- **Nhược điểm:** Số lượng ít

### 2. `pois_hcm_extended.csv` - Dataset Mở Rộng ⭐
- **Số lượng:** 177 POIs
- **Nguồn:** OpenStreetMap (Overpass API)
- **Ưu điểm:** Nhiều địa điểm, đa dạng
- **Phân loại:**
  - 🍽️ Nhà hàng: 46 POIs
  - 🏛️ Di tích lịch sử: 24 POIs
  - 🌳 Công viên: 24 POIs
  - 🛕 Tôn giáo: 20 POIs
  - 🏛️ Bảo tàng: 19 POIs
  - 🛍️ Mua sắm: 14 POIs
  - 🎭 Giải trí: 21 POIs
  - 🌆 Điểm ngắm cảnh: 9 POIs

## 🚀 Cách Sử Dụng

### Trong Code (Mặc Định)
File `pages/page_chuc_nang.py` đã được cập nhật để dùng dataset mở rộng:

```python
csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "pois_hcm_extended.csv")
pois = load_pois(csv_path)  # Sẽ load 177 POIs
```

### Đổi Về Dataset Gốc (Nếu Cần)
Nếu muốn dùng dataset nhỏ hơn:

```python
csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "pois_hcm.csv")
pois = load_pois(csv_path)  # Sẽ load 20 POIs
```

## 🔄 Cập Nhật Dữ Liệu Mới

### Tự Động Từ OpenStreetMap

Chạy script để lấy dữ liệu mới nhất:

```bash
python scripts/fetch_pois_osm.py
```

Script này sẽ:
1. Query OpenStreetMap qua Overpass API
2. Lấy các loại POI: museum, park, restaurant, shopping, religious, v.v.
3. Loại bỏ duplicate
4. Thêm metadata: rating, visit duration, entry fee, opening hours
5. Lưu vào `data/pois_hcm_extended.csv`

### Thủ Công

Chỉnh sửa file CSV trực tiếp, format:

```csv
id,name,lat,lon,tags,rating,visit_duration_min,entry_fee,open_hour,close_hour
1,Tên địa điểm,10.7797,106.6990,history;landmark,4.5,45,0,8,17
```

**Lưu ý:**
- `tags`: Dùng dấu `;` để phân cách (ví dụ: `history;museum;culture`)
- `rating`: 0.0 - 5.0
- `visit_duration_min`: Thời gian tham quan (phút)
- `entry_fee`: Phí vào cửa (VND), 0 nếu miễn phí
- `open_hour`, `close_hour`: Giờ mở/đóng cửa (0-23)

## 📝 Cấu Trúc Dữ Liệu

| Cột | Kiểu | Mô tả | Ví dụ |
|-----|------|-------|-------|
| `id` | int | ID duy nhất | 1 |
| `name` | string | Tên địa điểm | "Nhà thờ Đức Bà" |
| `lat` | float | Vĩ độ | 10.7797 |
| `lon` | float | Kinh độ | 106.6990 |
| `tags` | string | Phân loại (`;` separated) | "history;landmark;religious" |
| `rating` | float | Đánh giá (0-5) | 4.5 |
| `visit_duration_min` | int | Thời gian tham quan (phút) | 45 |
| `entry_fee` | int | Phí vào cửa (VND) | 40000 |
| `open_hour` | int | Giờ mở cửa (0-23) | 8 |
| `close_hour` | int | Giờ đóng cửa (0-23) | 17 |

## 🏷️ Tags (Phân Loại)

Các tag được dùng trong algo1 để match với preference của user:

- `history`: Di tích lịch sử
- `museum`: Bảo tàng
- `culture`: Văn hóa
- `food`: Ẩm thực
- `restaurant`: Nhà hàng
- `park`: Công viên
- `nature`: Thiên nhiên
- `shopping`: Mua sắm
- `entertainment`: Giải trí
- `religious`: Tôn giáo
- `landmark`: Địa danh nổi tiếng
- `viewpoint`: Điểm ngắm cảnh
- `modern`: Hiện đại
- `architecture`: Kiến trúc
- `nightlife`: Cuộc sống đêm

## 🌐 APIs Sử Dụng

### Overpass API (OpenStreetMap)
- **Endpoint:** `https://overpass-api.de/api/interpreter`
- **Docs:** https://wiki.openstreetmap.org/wiki/Overpass_API
- **Rate Limit:** ~2 requests/giây
- **Miễn phí:** Không cần API key

### Alternative APIs (Nếu Cần Mở Rộng)

1. **Google Places API**
   - Nhiều dữ liệu hơn (reviews, photos, phone)
   - **Yêu cầu:** API key
   - **Giá:** $17/1000 requests

2. **Foursquare API**
   - Dữ liệu venue tốt
   - **Yêu cầu:** API key
   - **Miễn phí:** 950 calls/day

3. **Yelp Fusion API**
   - Tốt cho nhà hàng
   - **Yêu cầu:** API key
   - **Miễn phí:** 5000 calls/day

## 💡 Tips

1. **Performance:** Dataset càng lớn, thuật toán chạy càng lâu. 177 POIs là optimal cho real-time response.

2. **Quality vs Quantity:** OpenStreetMap data có thể thiếu info (rating, opening hours). Cân nhắc việc dọn dẹp hoặc bổ sung thủ công.

3. **Geo Coverage:** Bbox hiện tại bao phủ toàn TP.HCM. Điều chỉnh trong `fetch_pois_osm.py` nếu cần thu hẹp/mở rộng.

4. **Incremental Updates:** Chạy script định kỳ (weekly) để cập nhật POIs mới từ OSM.

## 🔍 Test Dataset

```bash
# Test load POIs
python test_extended_pois.py

# Output:
# ✓ Loaded 177 POIs
#   - Museums: 19
#   - Restaurants: 46
#   - Parks: 24
#   - Religious: 20
```

## 📚 Tài Liệu Tham Khảo

- [OpenStreetMap Wiki](https://wiki.openstreetmap.org/)
- [Overpass Turbo](https://overpass-turbo.eu/) - Test queries
- [OSM Tags](https://wiki.openstreetmap.org/wiki/Map_features) - Danh sách tag đầy đủ
