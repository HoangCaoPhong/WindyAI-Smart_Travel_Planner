# Manual Test Cases - Algo5 Suggester
# Hướng dẫn test thủ công cho thuật toán gợi ý địa điểm

## 🎯 Mục đích
Test thủ công các chức năng của Algo5 Suggester với input/output cụ thể

## 📋 Chuẩn bị
- Đảm bảo file `core/algo5/algo5_suggester.py` tồn tại
- Chuẩn bị dữ liệu POI mẫu
- Có Python environment đã cài đặt dependencies

---

## TEST CASE 1: Khoảng cách giữa hai điểm giống nhau

### Input:
```python
from core.algo5.algo5_suggester import haversine

lat1 = 10.7769
lon1 = 106.7009
lat2 = 10.7769
lon2 = 106.7009

result = haversine(lat1, lon1, lat2, lon2)
```

### Expected Output:
```
0.0 hoặc rất gần 0
```

### Cách test:
1. Mở Python terminal
2. Chạy code trên
3. Kiểm tra `result == 0` hoặc `result < 0.001`

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 2: Khoảng cách Sài Gòn - Hà Nội

### Input:
```python
from core.algo5.algo5_suggester import haversine

# Sài Gòn
lat1 = 10.7769
lon1 = 106.7009

# Hà Nội
lat2 = 21.0285
lon2 = 105.8542

result = haversine(lat1, lon1, lat2, lon2)
print(f"Khoảng cách SG-HN: {result:.2f} km")
```

### Expected Output:
```
Khoảng cách SG-HN: ~1160 km (trong khoảng 1100-1200 km)
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 3: Gợi ý địa điểm với đủ thời gian và ngân sách

### Input:
```python
from core.algo5.algo5_suggester import suggest_places
from datetime import datetime

# Vị trí hiện tại: Trung tâm Sài Gòn
current_loc = (10.7769, 106.7009)

# Thời gian: 9h sáng đến 6h chiều
current_time = datetime(2025, 11, 30, 9, 0)
end_time = datetime(2025, 11, 30, 18, 0)

# Ngân sách: 500k VND
budget_left = 500000

# Số lượng gợi ý: 5
K = 5

# Preferences
prefs = {
    "museum": 0.8,
    "religion": 0.6,
    "shopping": 0.4,
    "food": 0.7
}

# Dữ liệu POI mẫu
pois = [
    {
        "id": 1,
        "name": "Nhà thờ Đức Bà",
        "lat": 10.7797,
        "lon": 106.6991,
        "category": "religion",
        "rating": 4.5,
        "cost": 0,
        "open_hour": 8,
        "close_hour": 17
    },
    {
        "id": 2,
        "name": "Bảo tàng Chứng tích Chiến tranh",
        "lat": 10.7796,
        "lon": 106.6918,
        "category": "museum",
        "rating": 4.6,
        "cost": 40000,
        "open_hour": 7,
        "close_hour": 18
    },
    {
        "id": 3,
        "name": "Chợ Bến Thành",
        "lat": 10.7729,
        "lon": 106.6981,
        "category": "shopping",
        "rating": 4.2,
        "cost": 0,
        "open_hour": 6,
        "close_hour": 22
    },
    {
        "id": 4,
        "name": "Phố ẩm thực Nguyễn Huệ",
        "lat": 10.7743,
        "lon": 106.7012,
        "category": "food",
        "rating": 4.3,
        "cost": 100000,
        "open_hour": 10,
        "close_hour": 23
    },
    {
        "id": 5,
        "name": "Dinh Độc Lập",
        "lat": 10.7769,
        "lon": 106.6950,
        "category": "museum",
        "rating": 4.4,
        "cost": 65000,
        "open_hour": 8,
        "close_hour": 16
    }
]

# Chạy thuật toán
results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, pois)

# In kết quả
print(f"\nSố lượng gợi ý: {len(results)}")
for i, r in enumerate(results, 1):
    print(f"\n{i}. {r['poi']['name']}")
    print(f"   - Điểm: {r['score']:.4f}")
    print(f"   - Khoảng cách: {r['dist']:.2f} km")
    print(f"   - Thời gian di chuyển: {r['travel_time_hours']*60:.0f} phút")
    print(f"   - Category: {r['poi']['category']}")
    print(f"   - Rating: {r['poi']['rating']}")
```

### Expected Output:
```
Số lượng gợi ý: 5 (hoặc ít hơn)

Danh sách được sắp xếp theo điểm giảm dần:
1. Bảo tàng Chứng tích Chiến tranh (museum - rating cao, preference cao)
2. Dinh Độc Lập (museum - preference cao)
3. Phở ẩm thực Nguyễn Huệ (food - preference tốt)
4. Nhà thờ Đức Bà (religion - miễn phí)
5. Chợ Bến Thành (shopping - preference thấp nhất)

Các POI phải:
- ✅ Nằm trong ngân sách (cost <= 500000)
- ✅ Mở cửa trong khung giờ 9h-18h
- ✅ Có thể đến được với tốc độ đi bộ 4km/h
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output:
_______________________________________________
_______________________________________________
```

---

## TEST CASE 4: Ngân sách = 0 (chỉ gợi ý miễn phí)

### Input:
```python
from core.algo5.algo5_suggester import suggest_places
from datetime import datetime

current_loc = (10.7769, 106.7009)
current_time = datetime(2025, 11, 30, 9, 0)
end_time = datetime(2025, 11, 30, 18, 0)
budget_left = 0  # Không có tiền
K = 5
prefs = {"museum": 0.8, "religion": 0.6, "shopping": 0.4}

pois = [
    {"id": 1, "name": "Nhà thờ Đức Bà", "lat": 10.7797, "lon": 106.6991,
     "category": "religion", "rating": 4.5, "cost": 0,
     "open_hour": 8, "close_hour": 17},
    {"id": 2, "name": "Bảo tàng (Có phí)", "lat": 10.7796, "lon": 106.6918,
     "category": "museum", "rating": 4.6, "cost": 40000,
     "open_hour": 7, "close_hour": 18},
    {"id": 3, "name": "Chợ Bến Thành", "lat": 10.7729, "lon": 106.6981,
     "category": "shopping", "rating": 4.2, "cost": 0,
     "open_hour": 6, "close_hour": 22}
]

results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, pois)

print(f"Số gợi ý: {len(results)}")
for r in results:
    print(f"- {r['poi']['name']} (Cost: {r['poi']['cost']} VND)")
```

### Expected Output:
```
Số gợi ý: 2

Chỉ gợi ý POI miễn phí:
- Nhà thờ Đức Bà (Cost: 0 VND)
- Chợ Bến Thành (Cost: 0 VND)

KHÔNG gợi ý:
- Bảo tàng (Có phí) - vì cost = 40000 > budget = 0
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 5: Thời gian rất ngắn (30 phút)

### Input:
```python
from core.algo5.algo5_suggester import suggest_places
from datetime import datetime

current_loc = (10.7769, 106.7009)
current_time = datetime(2025, 11, 30, 9, 0)
end_time = datetime(2025, 11, 30, 9, 30)  # Chỉ 30 phút
budget_left = 500000
K = 5
prefs = {"museum": 1.0}

pois = [
    {"id": 1, "name": "POI rất gần", "lat": 10.7770, "lon": 106.7010,
     "category": "museum", "rating": 4.5, "cost": 0,
     "open_hour": 8, "close_hour": 20},
    {"id": 2, "name": "POI xa", "lat": 10.8500, "lon": 106.8000,
     "category": "museum", "rating": 5.0, "cost": 0,
     "open_hour": 8, "close_hour": 20}
]

results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, pois)

print(f"Số gợi ý: {len(results)}")
for r in results:
    print(f"- {r['poi']['name']} (Travel: {r['travel_time_hours']*60:.0f} phút)")
```

### Expected Output:
```
Số gợi ý: 0 hoặc 1

Có thể gợi ý:
- POI rất gần (nếu có thể đến trong vòng 30 phút)

KHÔNG gợi ý:
- POI xa (vì mất hơn 30 phút để đến)
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 6: Tất cả POI đóng cửa

### Input:
```python
from core.algo5.algo5_suggester import suggest_places
from datetime import datetime

current_loc = (10.7769, 106.7009)
current_time = datetime(2025, 11, 30, 23, 0)  # 11h đêm
end_time = datetime(2025, 11, 30, 23, 59)
budget_left = 500000
K = 5
prefs = {"museum": 1.0}

pois = [
    {"id": 1, "name": "Museum A", "lat": 10.7770, "lon": 106.7010,
     "category": "museum", "rating": 4.5, "cost": 0,
     "open_hour": 8, "close_hour": 17},  # Đóng cửa lúc 5h chiều
    {"id": 2, "name": "Museum B", "lat": 10.7780, "lon": 106.7020,
     "category": "museum", "rating": 4.6, "cost": 0,
     "open_hour": 9, "close_hour": 18}   # Đóng cửa lúc 6h chiều
]

results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, pois)

print(f"Số gợi ý: {len(results)}")
```

### Expected Output:
```
Số gợi ý: 0

Không có gợi ý vì tất cả POI đều đã đóng cửa
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 7: K lớn hơn số lượng POI

### Input:
```python
from core.algo5.algo5_suggester import suggest_places
from datetime import datetime

current_loc = (10.7769, 106.7009)
current_time = datetime(2025, 11, 30, 9, 0)
end_time = datetime(2025, 11, 30, 18, 0)
budget_left = 500000
K = 100  # Yêu cầu 100 gợi ý
prefs = {"museum": 1.0}

pois = [
    {"id": 1, "name": "POI 1", "lat": 10.7770, "lon": 106.7010,
     "category": "museum", "rating": 4.5, "cost": 0,
     "open_hour": 8, "close_hour": 20},
    {"id": 2, "name": "POI 2", "lat": 10.7780, "lon": 106.7020,
     "category": "museum", "rating": 4.6, "cost": 0,
     "open_hour": 8, "close_hour": 20}
]

results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, pois)

print(f"K = {K}")
print(f"Số POI khả dụng: {len(pois)}")
print(f"Số gợi ý thực tế: {len(results)}")
```

### Expected Output:
```
K = 100
Số POI khả dụng: 2
Số gợi ý thực tế: 2

Chỉ trả về tối đa số POI khả dụng, không vượt quá
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 8: K = 0

### Input:
```python
from core.algo5.algo5_suggester import suggest_places
from datetime import datetime

current_loc = (10.7769, 106.7009)
current_time = datetime(2025, 11, 30, 9, 0)
end_time = datetime(2025, 11, 30, 18, 0)
budget_left = 500000
K = 0  # Không yêu cầu gợi ý
prefs = {"museum": 1.0}

pois = [
    {"id": 1, "name": "POI 1", "lat": 10.7770, "lon": 106.7010,
     "category": "museum", "rating": 4.5, "cost": 0,
     "open_hour": 8, "close_hour": 20}
]

results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, pois)

print(f"Số gợi ý: {len(results)}")
```

### Expected Output:
```
Số gợi ý: 0

Trả về danh sách rỗng vì K = 0
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 9: Preferences rỗng

### Input:
```python
from core.algo5.algo5_suggester import suggest_places
from datetime import datetime

current_loc = (10.7769, 106.7009)
current_time = datetime(2025, 11, 30, 9, 0)
end_time = datetime(2025, 11, 30, 18, 0)
budget_left = 500000
K = 3
prefs = {}  # Không có preference nào

pois = [
    {"id": 1, "name": "Museum", "lat": 10.7770, "lon": 106.7010,
     "category": "museum", "rating": 4.5, "cost": 0,
     "open_hour": 8, "close_hour": 20},
    {"id": 2, "name": "Park", "lat": 10.7780, "lon": 106.7020,
     "category": "park", "rating": 4.3, "cost": 0,
     "open_hour": 6, "close_hour": 22}
]

results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, pois)

print(f"Số gợi ý: {len(results)}")
for r in results:
    print(f"- {r['poi']['name']} (Score: {r['score']:.4f})")
```

### Expected Output:
```
Số gợi ý: 2

Vẫn hoạt động, score dựa trên:
- Khoảng cách (40%)
- Rating (30%)
- Preference = 0 vì không có trong prefs (30%)

POI gần hơn và rating cao hơn sẽ có điểm cao hơn
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 10: Preference ảnh hưởng đến điểm

### Input:
```python
from core.algo5.algo5_suggester import suggest_places
from datetime import datetime

current_loc = (10.7769, 106.7009)
current_time = datetime(2025, 11, 30, 9, 0)
end_time = datetime(2025, 11, 30, 18, 0)
budget_left = 500000
K = 3

# Ưu tiên museum rất cao
prefs = {"museum": 1.0, "park": 0.1}

pois = [
    {"id": 1, "name": "Museum", "lat": 10.7770, "lon": 106.7010,
     "category": "museum", "rating": 4.0, "cost": 0,
     "open_hour": 8, "close_hour": 20},
    {"id": 2, "name": "Park", "lat": 10.7770, "lon": 106.7010,  # Cùng vị trí
     "category": "park", "rating": 4.0, "cost": 0,
     "open_hour": 8, "close_hour": 20}
]

results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, pois)

print("\nSắp xếp theo điểm:")
for i, r in enumerate(results, 1):
    print(f"{i}. {r['poi']['name']} - Score: {r['score']:.4f}")
```

### Expected Output:
```
Sắp xếp theo điểm:
1. Museum - Score: > 0.6
2. Park - Score: < 0.5

Museum phải có điểm cao hơn Park vì preference cao hơn
(cùng vị trí, cùng rating nhưng preference khác nhau)
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 11: Lọc theo giờ mở cửa buổi sáng

### Input:
```python
from core.algo5.algo5_suggester import suggest_places
from datetime import datetime

current_loc = (10.7769, 106.7009)
current_time = datetime(2025, 11, 30, 7, 0)  # 7h sáng
end_time = datetime(2025, 11, 30, 9, 0)
budget_left = 500000
K = 5
prefs = {"food": 1.0, "museum": 1.0}

pois = [
    {"id": 1, "name": "Quán phở (mở sáng)", "lat": 10.7770, "lon": 106.7010,
     "category": "food", "rating": 4.5, "cost": 50000,
     "open_hour": 6, "close_hour": 10},  # Chỉ mở buổi sáng
    {"id": 2, "name": "Museum (mở muộn)", "lat": 10.7780, "lon": 106.7020,
     "category": "museum", "rating": 4.6, "cost": 0,
     "open_hour": 9, "close_hour": 17},  # Mở từ 9h
    {"id": 3, "name": "Park (mở cả ngày)", "lat": 10.7790, "lon": 106.7030,
     "category": "park", "rating": 4.0, "cost": 0,
     "open_hour": 0, "close_hour": 23}
]

results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, pois)

print(f"Thời gian hiện tại: 7h sáng")
print(f"Số gợi ý: {len(results)}")
for r in results:
    print(f"- {r['poi']['name']} (Mở: {r['poi']['open_hour']}h)")
```

### Expected Output:
```
Thời gian hiện tại: 7h sáng
Số gợi ý: 2 hoặc 3

Được gợi ý:
- Quán phở (đang mở)
- Park (đang mở)

Có thể KHÔNG gợi ý:
- Museum (chưa mở cửa vào lúc 7h)
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 12: Lọc theo giờ mở cửa buổi tối

### Input:
```python
from core.algo5.algo5_suggester import suggest_places
from datetime import datetime

current_loc = (10.7769, 106.7009)
current_time = datetime(2025, 11, 30, 19, 0)  # 7h tối
end_time = datetime(2025, 11, 30, 22, 0)
budget_left = 500000
K = 5
prefs = {"entertainment": 1.0, "museum": 1.0}

pois = [
    {"id": 1, "name": "Museum (đóng cửa sớm)", "lat": 10.7770, "lon": 106.7010,
     "category": "museum", "rating": 4.5, "cost": 0,
     "open_hour": 8, "close_hour": 17},  # Đóng từ 5h chiều
    {"id": 2, "name": "Bar (mở tối)", "lat": 10.7780, "lon": 106.7020,
     "category": "entertainment", "rating": 4.3, "cost": 100000,
     "open_hour": 18, "close_hour": 23}  # Mở từ 6h tối
]

results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, pois)

print(f"Thời gian hiện tại: 7h tối")
print(f"Số gợi ý: {len(results)}")
for r in results:
    print(f"- {r['poi']['name']}")
```

### Expected Output:
```
Thời gian hiện tại: 7h tối
Số gợi ý: 1

Được gợi ý:
- Bar (đang mở)

KHÔNG gợi ý:
- Museum (đã đóng cửa)
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 13: Vị trí rất xa (không thể đến kịp)

### Input:
```python
from core.algo5.algo5_suggester import suggest_places
from datetime import datetime

current_loc = (21.0285, 105.8542)  # Hà Nội
current_time = datetime(2025, 11, 30, 9, 0)
end_time = datetime(2025, 11, 30, 18, 0)
budget_left = 500000
K = 5
prefs = {"museum": 1.0}

pois = [
    {"id": 1, "name": "POI ở Sài Gòn", "lat": 10.7769, "lon": 106.7009,
     "category": "museum", "rating": 5.0, "cost": 0,
     "open_hour": 8, "close_hour": 20}
]

results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, pois)

print(f"Vị trí hiện tại: Hà Nội")
print(f"POI ở: Sài Gòn (~1160 km)")
print(f"Số gợi ý: {len(results)}")
```

### Expected Output:
```
Vị trí hiện tại: Hà Nội
POI ở: Sài Gòn (~1160 km)
Số gợi ý: 0

Không có gợi ý vì:
- Khoảng cách quá xa (~1160 km)
- Với tốc độ đi bộ 4km/h, cần ~290 giờ
- Không thể đến được trong khung giờ 9h-18h (9 giờ)
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 14: POI gần được ưu tiên hơn

### Input:
```python
from core.algo5.algo5_suggester import suggest_places
from datetime import datetime

current_loc = (10.7769, 106.7009)
current_time = datetime(2025, 11, 30, 9, 0)
end_time = datetime(2025, 11, 30, 18, 0)
budget_left = 500000
K = 3
prefs = {"museum": 1.0}

pois = [
    {"id": 1, "name": "Museum gần (100m)", "lat": 10.7770, "lon": 106.7010,
     "category": "museum", "rating": 4.0, "cost": 0,
     "open_hour": 8, "close_hour": 20},
    {"id": 2, "name": "Museum xa (10km)", "lat": 10.8500, "lon": 106.7500,
     "category": "museum", "rating": 4.0, "cost": 0,
     "open_hour": 8, "close_hour": 20}
]

results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, pois)

print("Sắp xếp theo điểm:")
for i, r in enumerate(results, 1):
    print(f"{i}. {r['poi']['name']}")
    print(f"   Distance: {r['dist']:.2f} km")
    print(f"   Score: {r['score']:.4f}")
```

### Expected Output:
```
Sắp xếp theo điểm:
1. Museum gần (100m)
   Distance: ~0.1 km
   Score: > 0.7

2. Museum xa (10km)
   Distance: ~10 km
   Score: < 0.5

POI gần hơn có điểm cao hơn (với cùng rating và preference)
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 15: Rating cao được ưu tiên

### Input:
```python
from core.algo5.algo5_suggester import suggest_places
from datetime import datetime

current_loc = (10.7769, 106.7009)
current_time = datetime(2025, 11, 30, 9, 0)
end_time = datetime(2025, 11, 30, 18, 0)
budget_left = 500000
K = 3
prefs = {"museum": 1.0}

pois = [
    {"id": 1, "name": "Museum rating thấp", "lat": 10.7770, "lon": 106.7010,
     "category": "museum", "rating": 3.0, "cost": 0,
     "open_hour": 8, "close_hour": 20},
    {"id": 2, "name": "Museum rating cao", "lat": 10.7770, "lon": 106.7010,
     "category": "museum", "rating": 5.0, "cost": 0,
     "open_hour": 8, "close_hour": 20}
]

results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, pois)

print("Sắp xếp theo điểm:")
for i, r in enumerate(results, 1):
    print(f"{i}. {r['poi']['name']}")
    print(f"   Rating: {r['poi']['rating']}")
    print(f"   Score: {r['score']:.4f}")
```

### Expected Output:
```
Sắp xếp theo điểm:
1. Museum rating cao
   Rating: 5.0
   Score: > 0.8

2. Museum rating thấp
   Rating: 3.0
   Score: < 0.7

POI có rating cao hơn được ưu tiên (với cùng vị trí và preference)
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 16: Lọc nghiêm ngặt theo ngân sách

### Input:
```python
from core.algo5.algo5_suggester import suggest_places
from datetime import datetime

current_loc = (10.7769, 106.7009)
current_time = datetime(2025, 11, 30, 9, 0)
end_time = datetime(2025, 11, 30, 18, 0)
budget_left = 50000  # Chỉ 50k
K = 5
prefs = {"museum": 1.0}

pois = [
    {"id": 1, "name": "POI miễn phí", "lat": 10.7770, "lon": 106.7010,
     "category": "museum", "rating": 4.0, "cost": 0,
     "open_hour": 8, "close_hour": 20},
    {"id": 2, "name": "POI 20k (rẻ)", "lat": 10.7780, "lon": 106.7020,
     "category": "museum", "rating": 4.5, "cost": 20000,
     "open_hour": 8, "close_hour": 20},
    {"id": 3, "name": "POI 100k (đắt)", "lat": 10.7790, "lon": 106.7030,
     "category": "museum", "rating": 5.0, "cost": 100000,
     "open_hour": 8, "close_hour": 20}
]

results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, pois)

print(f"Ngân sách: {budget_left} VND")
print(f"Số gợi ý: {len(results)}")
for r in results:
    print(f"- {r['poi']['name']} (Cost: {r['poi']['cost']} VND)")
```

### Expected Output:
```
Ngân sách: 50000 VND
Số gợi ý: 2

Được gợi ý:
- POI miễn phí (Cost: 0 VND) ✅
- POI 20k (Cost: 20000 VND) ✅

KHÔNG gợi ý:
- POI 100k (Cost: 100000 VND) ❌ - vượt ngân sách
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 17: Ngân sách âm

### Input:
```python
from core.algo5.algo5_suggester import suggest_places
from datetime import datetime

current_loc = (10.7769, 106.7009)
current_time = datetime(2025, 11, 30, 9, 0)
end_time = datetime(2025, 11, 30, 18, 0)
budget_left = -10000  # Ngân sách âm
K = 5
prefs = {"park": 1.0}

pois = [
    {"id": 1, "name": "Park miễn phí", "lat": 10.7770, "lon": 106.7010,
     "category": "park", "rating": 4.0, "cost": 0,
     "open_hour": 6, "close_hour": 22}
]

results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, pois)

print(f"Ngân sách: {budget_left} VND")
print(f"Số gợi ý: {len(results)}")
```

### Expected Output:
```
Ngân sách: -10000 VND
Số gợi ý: 0

Không có gợi ý vì ngân sách âm (không hợp lệ)
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 18: Kết quả được sắp xếp theo điểm giảm dần

### Input:
```python
from core.algo5.algo5_suggester import suggest_places
from datetime import datetime

current_loc = (10.7769, 106.7009)
current_time = datetime(2025, 11, 30, 9, 0)
end_time = datetime(2025, 11, 30, 18, 0)
budget_left = 500000
K = 5
prefs = {"museum": 1.0}

pois = [
    {"id": 1, "name": "POI A", "lat": 10.7800, "lon": 106.7100,
     "category": "museum", "rating": 3.5, "cost": 0,
     "open_hour": 8, "close_hour": 20},
    {"id": 2, "name": "POI B", "lat": 10.7770, "lon": 106.7010,
     "category": "museum", "rating": 5.0, "cost": 0,
     "open_hour": 8, "close_hour": 20},
    {"id": 3, "name": "POI C", "lat": 10.7780, "lon": 106.7020,
     "category": "museum", "rating": 4.2, "cost": 0,
     "open_hour": 8, "close_hour": 20}
]

results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, pois)

print("Kiểm tra sắp xếp:")
scores = [r['score'] for r in results]
is_sorted = all(scores[i] >= scores[i+1] for i in range(len(scores)-1))
print(f"Scores: {[f'{s:.4f}' for s in scores]}")
print(f"Đã sắp xếp giảm dần: {is_sorted}")
```

### Expected Output:
```
Kiểm tra sắp xếp:
Scores: [0.xxxx, 0.yyyy, 0.zzzz]
Đã sắp xếp giảm dần: True

Điểm phải giảm dần từ trên xuống dưới
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 19: Trường hợp không có POI khả dụng

### Input:
```python
from core.algo5.algo5_suggester import suggest_places
from datetime import datetime

current_loc = (10.7769, 106.7009)
current_time = datetime(2025, 11, 30, 9, 0)
end_time = datetime(2025, 11, 30, 18, 0)
budget_left = 500000
K = 5
prefs = {"museum": 1.0}

pois = []  # Không có POI nào

results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, pois)

print(f"Số POI trong database: {len(pois)}")
print(f"Số gợi ý: {len(results)}")
print(f"Kết quả: {results}")
```

### Expected Output:
```
Số POI trong database: 0
Số gợi ý: 0
Kết quả: []

Trả về danh sách rỗng khi không có POI nào
```

### Kết quả: ✅ PASS / ❌ FAIL
```
Actual Output: _____________
```

---

## TEST CASE 20: Test tích hợp hoàn chỉnh

### Input:
```python
from core.algo5.algo5_suggester import suggest_places
from datetime import datetime

# Scenario: Du khách có 4 giờ (2pm - 6pm), budget 300k
current_loc = (10.7769, 106.7009)  # Trung tâm Sài Gòn
current_time = datetime(2025, 11, 30, 14, 0)  # 2 PM
end_time = datetime(2025, 11, 30, 18, 0)      # 6 PM
budget_left = 300000  # 300k VND
K = 3  # Top 3 gợi ý

prefs = {
    "culture": 0.9,
    "food": 0.7,
    "shopping": 0.3
}

pois = [
    {"id": 1, "name": "Nhà hát Thành phố", "lat": 10.7769, "lon": 106.7024,
     "category": "culture", "rating": 4.7, "cost": 150000,
     "open_hour": 9, "close_hour": 21},
    {"id": 2, "name": "Phố đi bộ Nguyễn Huệ", "lat": 10.7743, "lon": 106.7012,
     "category": "culture", "rating": 4.4, "cost": 0,
     "open_hour": 0, "close_hour": 23},
    {"id": 3, "name": "Bitexco Tower", "lat": 10.7716, "lon": 106.7037,
     "category": "culture", "rating": 4.5, "cost": 200000,
     "open_hour": 9, "close_hour": 22},
    {"id": 4, "name": "Chợ đêm", "lat": 10.7650, "lon": 106.6900,
     "category": "shopping", "rating": 4.0, "cost": 0,
     "open_hour": 18, "close_hour": 23},
    {"id": 5, "name": "Quán ăn địa phương", "lat": 10.7750, "lon": 106.7000,
     "category": "food", "rating": 4.6, "cost": 80000,
     "open_hour": 11, "close_hour": 22}
]

results = suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, pois)

print("=" * 60)
print("TRAVEL SUGGESTION REPORT")
print("=" * 60)
print(f"📍 Vị trí hiện tại: {current_loc}")
print(f"⏰ Thời gian: {current_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}")
print(f"💰 Ngân sách: {budget_left:,} VND")
print(f"🎯 Top {K} gợi ý")
print("=" * 60)

total_cost = 0
for i, r in enumerate(results, 1):
    print(f"\n{i}. {r['poi']['name']}")
    print(f"   📊 Điểm: {r['score']:.4f}")
    print(f"   ⭐ Rating: {r['poi']['rating']}/5.0")
    print(f"   📏 Khoảng cách: {r['dist']:.2f} km")
    print(f"   🚶 Thời gian đi: {r['travel_time_hours']*60:.0f} phút")
    print(f"   💵 Chi phí: {r['poi']['cost']:,} VND")
    print(f"   🏷️ Loại: {r['poi']['category']}")
    total_cost += r['poi']['cost']

print("\n" + "=" * 60)
print(f"Tổng chi phí dự kiến: {total_cost:,} VND")
print(f"Còn lại: {budget_left - total_cost:,} VND")
print("=" * 60)
```

### Expected Output:
```
============================================================
TRAVEL SUGGESTION REPORT
============================================================
📍 Vị trí hiện tại: (10.7769, 106.7009)
⏰ Thời gian: 14:00 - 18:00
💰 Ngân sách: 300,000 VND
🎯 Top 3 gợi ý
============================================================

1. Phố đi bộ Nguyễn Huệ (hoặc POI culture khác)
   📊 Điểm: 0.xxxx
   ⭐ Rating: 4.4/5.0
   📏 Khoảng cách: ~0.3 km
   🚶 Thời gian đi: ~5 phút
   💵 Chi phí: 0 VND
   🏷️ Loại: culture

2. Nhà hát Thành phố hoặc Quán ăn địa phương
   📊 Điểm: 0.yyyy
   ...

3. [POI thứ 3]
   ...

============================================================
Tổng chi phí dự kiến: < 300,000 VND
Còn lại: > 0 VND
============================================================

Kiểm tra:
✅ Tất cả POI trong budget
✅ Tất cả POI đang mở cửa (2PM - 6PM)
✅ POI culture được ưu tiên (preference = 0.9)
✅ Bitexco có thể không được gợi ý (200k, vượt budget nếu kết hợp với POI khác)
✅ Chợ đêm không được gợi ý (mở cửa từ 6PM)
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
- [ ] Logic tính khoảng cách sai
- [ ] Lọc theo thời gian không chính xác
- [ ] Lọc theo ngân sách không chính xác
- [ ] Sắp xếp điểm sai
- [ ] Edge cases không xử lý
- [ ] Khác: _________________

### Ghi chú
```
_________________________________________________
_________________________________________________
_________________________________________________
```

---

## 🔧 Hướng dẫn sử dụng

1. **Chuẩn bị**: Đảm bảo code đã được implement
2. **Copy code**: Copy từng test case vào Python terminal
3. **Chạy**: Execute và quan sát output
4. **So sánh**: So sánh Actual vs Expected Output
5. **Đánh dấu**: Đánh dấu ✅ PASS hoặc ❌ FAIL
6. **Ghi chú**: Ghi lại lỗi nếu FAIL

### Tips
- Chạy từng test một để dễ debug
- Lưu output vào file text để tham khảo
- Nếu test FAIL, kiểm tra lại implementation
- Test case có thể adjust theo business logic thực tế
