# MANUAL TEST CASES - Smart Travel Project
# Hướng dẫn test thủ công với input và output cụ thể

## TEST CASE 1: Tính khoảng cách giữa 2 địa điểm
**Mục đích**: Kiểm tra hàm tính khoảng cách Haversine

**Input**:
```python
from core.utils_geo import haversine_km

# Chợ Bến Thành → Nhà thờ Đức Bà
loc_a = (10.7729, 106.6981)  # Chợ Bến Thành
loc_b = (10.7797, 106.6991)  # Nhà thờ Đức Bà

distance = haversine_km(loc_a, loc_b)
print(f"Khoảng cách: {distance:.2f} km")
```

**Output mong đợi**:
```
Khoảng cách: 0.76 km
```

**Cách test**: Copy code trên vào Python console và chạy

---

## TEST CASE 2: Tính chi phí di chuyển
**Mục đích**: Kiểm tra tính toán thời gian và chi phí cho các phương tiện

**Input**:
```python
from core.utils_geo import travel_info

loc_a = (10.7729, 106.6981)  # Chợ Bến Thành
loc_b = (10.7797, 106.6991)  # Nhà thờ Đức Bà

# Test với 3 phương tiện
for mode in ["walking", "motorbike", "taxi"]:
    dist, time_min, cost = travel_info(loc_a, loc_b, mode)
    print(f"{mode:10s}: {dist:.2f}km, {time_min:.1f} phút, {cost:.0f}đ")
```

**Output mong đợi**:
```
walking   : 0.76km, 9.1 phút, 0đ
motorbike : 0.76km, 1.8 phút, 1520đ
taxi      : 0.76km, 1.3 phút, 9120đ
```

---

## TEST CASE 3: Đánh giá độ khớp sở thích
**Mục đích**: Kiểm tra hàm tính điểm sở thích

**Input**:
```python
from core.scorer import preference_score

# Test 1: Khớp hoàn hảo
tags = ["museum", "historical", "cultural"]
prefs = ["museum", "historical", "cultural"]
score1 = preference_score(tags, prefs)
print(f"Khớp hoàn hảo: {score1}")

# Test 2: Khớp một phần
tags = ["museum", "historical", "art"]
prefs = ["museum", "beach"]
score2 = preference_score(tags, prefs)
print(f"Khớp 1/2: {score2}")

# Test 3: Không khớp
tags = ["museum", "art"]
prefs = ["beach", "adventure"]
score3 = preference_score(tags, prefs)
print(f"Không khớp: {score3}")
```

**Output mong đợi**:
```
Khớp hoàn hảo: 1.0
Khớp 1/2: 0.5
Không khớp: 0.0
```

---

## TEST CASE 4: Đánh giá điểm POI
**Mục đích**: So sánh điểm số giữa các POI

**Input**:
```python
from core.scorer import score_candidate

poi1 = {
    "id": 1,
    "name": "Bảo tàng Chiến tranh",
    "rating": 4.7,
    "tags": ["museum", "historical"],
    "visit_duration_min": 120,
    "entry_fee": 40000
}

poi2 = {
    "id": 2,
    "name": "Chợ Bến Thành",
    "rating": 4.5,
    "tags": ["market", "shopping"],
    "visit_duration_min": 90,
    "entry_fee": 0
}

prefs = ["museum", "historical"]

score1 = score_candidate(poi1, travel_min=10, travel_cost=5000, user_prefs=prefs)
score2 = score_candidate(poi2, travel_min=10, travel_cost=5000, user_prefs=prefs)

print(f"Bảo tàng (có sở thích): {score1:.2f}")
print(f"Chợ (không sở thích): {score2:.2f}")
print(f"→ {'Bảo tàng' if score1 < score2 else 'Chợ'} được ưu tiên (điểm thấp hơn)")
```

**Output mong đợi**:
```
Bảo tàng (có sở thích): 63.01
Chợ (không sở thích): 110.01
→ Bảo tàng được ưu tiên (điểm thấp hơn)
```

---

## TEST CASE 5: Load dữ liệu POI từ CSV
**Mục đích**: Kiểm tra đọc và parse CSV

**Input**:
Tạo file `test_manual.csv`:
```csv
id,name,lat,lon,open_hour,close_hour,visit_duration_min,entry_fee,rating,tags
1,Chợ Bến Thành,10.7729,106.6981,7,19,90,0,4.5,market;shopping;cultural
2,Nhà thờ Đức Bà,10.7797,106.6991,8,18,45,0,4.6,historical;architectural
```

Chạy code:
```python
from core.solver_route import load_pois

pois = load_pois("test_manual.csv")

for poi in pois:
    print(f"ID: {poi['id']}")
    print(f"Tên: {poi['name']}")
    print(f"Tags: {poi['tags']}")
    print(f"Giờ mở: {poi['open_hour']}h - {poi['close_hour']}h")
    print()
```

**Output mong đợi**:
```
ID: 1
Tên: Chợ Bến Thành
Tags: ['market', 'shopping', 'cultural']
Giờ mở: 7h - 19h

ID: 2
Tên: Nhà thờ Đức Bà
Tags: ['historical', 'architectural']
Giờ mở: 8h - 18h
```

---

## TEST CASE 6: Lập kế hoạch tuyến đường đơn giản
**Mục đích**: Test thuật toán lập kế hoạch cơ bản

**Input**:
Tạo file `test_route.csv`:
```csv
id,name,lat,lon,open_hour,close_hour,visit_duration_min,entry_fee,rating,tags
1,Chợ Bến Thành,10.7729,106.6981,7,19,90,0,4.5,market;shopping
2,Nhà thờ Đức Bà,10.7797,106.6991,8,18,45,0,4.6,historical;cultural
3,Bưu điện TP,10.7799,106.6990,8,18,30,0,4.4,historical;architectural
```

Chạy code:
```python
from core.solver_route import load_pois, plan_route

pois = load_pois("test_route.csv")

route = plan_route(
    pois,
    user_prefs=["historical", "cultural"],
    start_loc=(10.7769, 106.7006),
    time_window=("2025-12-01 09:00", "2025-12-01 15:00"),
    budget=200000
)

print(f"Số điểm tham quan: {len(route)}")
print()

for i, step in enumerate(route, 1):
    print(f"{i}. {step['name']}")
    print(f"   Đến: {step['arrive_time'].strftime('%H:%M')}")
    print(f"   Đi: {step['depart_time'].strftime('%H:%M')}")
    print(f"   Phương tiện: {step['mode']}")
    print(f"   Chi phí: {int(step['travel_cost'] + step['entry_fee'])}đ")
    print()
```

**Output mong đợi**:
```
Số điểm tham quan: 3

1. Nhà thờ Đức Bà
   Đến: 09:02
   Đi: 09:47
   Phương tiện: walking
   Chi phí: 0đ

2. Bưu điện TP
   Đến: 09:47
   Đi: 10:17
   Phương tiện: walking
   Chi phí: 0đ

3. Chợ Bến Thành
   Đến: 10:19
   Đi: 11:49
   Phương tiện: walking
   Chi phí: 0đ
```

---

## TEST CASE 7: Ràng buộc ngân sách
**Mục đích**: Kiểm tra hệ thống tôn trọng ngân sách

**Input**:
```python
from core.solver_route import load_pois, plan_route

# Sử dụng cùng CSV test_route.csv ở trên
pois = load_pois("test_route.csv")

# Test với ngân sách thấp
route = plan_route(
    pois,
    user_prefs=[],
    start_loc=(10.7769, 106.7006),
    time_window=("2025-12-01 09:00", "2025-12-01 18:00"),
    budget=10000  # Chỉ 10k VND
)

total_cost = sum(step['travel_cost'] + step['entry_fee'] for step in route)

print(f"Ngân sách: 10,000đ")
print(f"Số điểm: {len(route)}")
print(f"Tổng chi phí: {int(total_cost):,}đ")
print(f"Còn lại: {10000 - int(total_cost):,}đ")
```

**Output mong đợi**:
```
Ngân sách: 10,000đ
Số điểm: 3
Tổng chi phí: 0đ
Còn lại: 10,000đ
```
*(Chỉ chọn các địa điểm miễn phí và đi bộ)*

---

## TEST CASE 8: Ràng buộc thời gian chặt
**Mục đích**: Kiểm tra ràng buộc cửa sổ thời gian

**Input**:
```python
from core.solver_route import load_pois, plan_route

pois = load_pois("test_route.csv")

# Cửa sổ thời gian rất hẹp: chỉ 2 tiếng
route = plan_route(
    pois,
    user_prefs=[],
    start_loc=(10.7769, 106.7006),
    time_window=("2025-12-01 09:00", "2025-12-01 11:00"),  # 2 giờ
    budget=500000
)

print(f"Cửa sổ: 09:00 - 11:00 (2 giờ)")
print(f"Số điểm: {len(route)}")

if route:
    start = route[0]['arrive_time']
    end = route[-1]['depart_time']
    print(f"Bắt đầu: {start.strftime('%H:%M')}")
    print(f"Kết thúc: {end.strftime('%H:%M')}")
    duration = (end - start).total_seconds() / 60
    print(f"Tổng thời gian: {int(duration)} phút")
```

**Output mong đợi**:
```
Cửa sổ: 09:00 - 11:00 (2 giờ)
Số điểm: 2
Bắt đầu: 09:02
Kết thúc: 10:17
Tổng thời gian: 75 phút
```

---

## TEST CASE 9: Ưu tiên theo sở thích
**Mục đích**: Kiểm tra thuật toán ưu tiên POI khớp sở thích

**Input**:
Tạo file `test_preference.csv`:
```csv
id,name,lat,lon,open_hour,close_hour,visit_duration_min,entry_fee,rating,tags
1,Bảo tàng Lịch sử,10.7870,106.7020,8,17,120,40000,4.7,museum;historical;educational
2,Công viên Tao Đàn,10.7750,106.6950,6,22,60,0,4.0,park;nature;relaxing
3,Bảo tàng Mỹ thuật,10.7690,106.7000,9,17,90,30000,4.5,museum;art;cultural
```

Chạy code:
```python
from core.solver_route import load_pois, plan_route

pois = load_pois("test_preference.csv")

route = plan_route(
    pois,
    user_prefs=["museum", "historical"],  # Thích bảo tàng, lịch sử
    start_loc=(10.7769, 106.7006),
    time_window=("2025-12-01 09:00", "2025-12-01 14:00"),
    budget=200000
)

print("Sở thích: museum, historical")
print(f"Số điểm: {len(route)}\n")

for i, step in enumerate(route, 1):
    poi = next(p for p in pois if p['id'] == step['id'])
    print(f"{i}. {step['name']}")
    print(f"   Tags: {', '.join(poi['tags'])}")
    print()
```

**Output mong đợi**:
```
Sở thích: museum, historical
Số điểm: 2

1. Bảo tàng Lịch sử
   Tags: museum, historical, educational

2. Bảo tàng Mỹ thuật
   Tags: museum, art, cultural
```
*(Công viên không được chọn vì không khớp sở thích)*

---

## TEST CASE 10: Kiểm tra giờ mở cửa
**Mục đích**: Đảm bảo không ghé POI ngoài giờ

**Input**:
Tạo file `test_hours.csv`:
```csv
id,name,lat,lon,open_hour,close_hour,visit_duration_min,entry_fee,rating,tags
1,Chợ sáng,10.7729,106.6981,6,12,90,0,4.2,market;local
2,Nhà hàng tối,10.7797,106.6991,18,23,120,150000,4.8,restaurant;dinner
3,Quán cafe,10.7799,106.7000,8,22,60,50000,4.4,cafe;coworking
```

Chạy code:
```python
from core.solver_route import load_pois, plan_route

pois = load_pois("test_hours.csv")

# Lập kế hoạch cho buổi chiều
route = plan_route(
    pois,
    user_prefs=[],
    start_loc=(10.7769, 106.7006),
    time_window=("2025-12-01 14:00", "2025-12-01 22:00"),
    budget=500000
)

print("Thời gian: 14:00 - 22:00 (chiều/tối)")
print(f"Số điểm: {len(route)}\n")

for step in route:
    poi = next(p for p in pois if p['id'] == step['id'])
    print(f"- {step['name']}")
    print(f"  Mở cửa: {poi['open_hour']}h - {poi['close_hour']}h")
    print(f"  Ghé thăm: {step['arrive_time'].strftime('%H:%M')} - {step['depart_time'].strftime('%H:%M')}")
    print()
```

**Output mong đợi**:
```
Thời gian: 14:00 - 22:00 (chiều/tối)
Số điểm: 2

- Quán cafe
  Mở cửa: 8h - 22h
  Ghé thăm: 14:02 - 15:02

- Nhà hàng tối
  Mở cửa: 18h - 23h
  Ghé thăm: 18:04 - 20:04
```
*(Chợ sáng không được chọn vì đóng cửa lúc 12h)*

---

## CÁCH SỬ DỤNG

### Bước 1: Mở Python console
```bash
cd d:\Downloads\SmartTravelProject-featureAI-algo1-solver\SmartTravelProject-featureAI-algo1-solver
python
```

### Bước 2: Copy từng test case và paste vào console

### Bước 3: So sánh output thực tế với output mong đợi

### Bước 4: Ghi nhận kết quả
- ✅ PASS: Output khớp với mong đợi
- ❌ FAIL: Output khác với mong đợi → Cần debug

---

## CHECKLIST TEST

- [ ] TC1: Tính khoảng cách
- [ ] TC2: Chi phí di chuyển  
- [ ] TC3: Độ khớp sở thích
- [ ] TC4: Điểm đánh giá POI
- [ ] TC5: Load CSV
- [ ] TC6: Lập kế hoạch cơ bản
- [ ] TC7: Ràng buộc ngân sách
- [ ] TC8: Ràng buộc thời gian
- [ ] TC9: Ưu tiên sở thích
- [ ] TC10: Giờ mở cửa

---

## LƯU Ý

1. **Độ chính xác số thực**: Output có thể chênh lệch nhỏ (±0.01) do làm tròn
2. **Thời gian**: Thời gian đến/đi có thể khác vài phút do tính toán travel time
3. **Thứ tự POI**: Có thể khác nếu nhiều POI có điểm số gần bằng nhau
4. **Phương tiện**: Thuật toán chọn phương tiện tối ưu nhất (thường là walking cho khoảng cách ngắn)
