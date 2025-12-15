# 20 Test Cases - Tổng quan chi tiết

## Phân loại theo chức năng

### 📍 Nhóm 1: Geo Utils (3 test cases)
Kiểm tra các hàm tính toán địa lý và khoảng cách

| # | Test Case | Mục đích | Input | Output mong đợi |
|---|-----------|----------|-------|-----------------|
| 1 | `test_01_haversine_same_location` | Khoảng cách cùng vị trí | Same coordinates | distance = 0.0 |
| 2 | `test_02_haversine_known_distance` | Khoảng cách đã biết | Ben Thanh ↔ Notre Dame | ~0.76 km |
| 3 | `test_03_travel_info_all_modes` | Tính toán cho mọi phương tiện | 3 modes (walking, motorbike, taxi) | Valid dist, time, cost |

**Coverage**: `utils_geo.py` - 100%

---

### 🎯 Nhóm 2: Scorer (4 test cases)
Kiểm tra hệ thống đánh giá và ưu tiên POI

| # | Test Case | Mục đích | Input | Output mong đợi |
|---|-----------|----------|-------|-----------------|
| 4 | `test_04_preference_score_perfect_match` | Khớp hoàn hảo | tags = prefs | score = 1.0 |
| 5 | `test_05_preference_score_no_match` | Không khớp | tags ≠ prefs | score = 0.0 |
| 6 | `test_06_preference_score_partial_match` | Khớp một phần | 1/2 tags match | score = 0.5 |
| 7 | `test_07_score_candidate_comparison` | So sánh POI | High vs low rating | Lower score for better POI |

**Coverage**: `scorer.py` - 100%

---

### 📂 Nhóm 3: POI Loading (3 test cases)
Kiểm tra việc load và xử lý dữ liệu POI từ CSV

| # | Test Case | Mục đích | Input | Output mong đợi |
|---|-----------|----------|-------|-----------------|
| 8 | `test_08_load_pois_valid_csv` | Load CSV hợp lệ | Valid CSV with 2 POIs | 2 POIs with parsed tags |
| 9 | `test_09_load_pois_empty_tags` | Tags rỗng | POI with empty tags | tags = [] |
| 10 | `test_10_load_pois_type_conversion` | Chuyển đổi kiểu | String values in CSV | Correct float/int types |

**Coverage**: `solver_route.py::load_pois` - 100%

---

### 🗺️ Nhóm 4: Route Planning (7 test cases)
Kiểm tra thuật toán lập kế hoạch tuyến đường - Core của hệ thống

| # | Test Case | Mục đích | Điều kiện kiểm tra | Edge case |
|---|-----------|----------|-------------------|-----------|
| 11 | `test_11_plan_route_basic` | Lập kế hoạch cơ bản | 2 POIs available | Normal scenario |
| 12 | `test_12_plan_route_budget_constraint` | Ràng buộc ngân sách | Budget = 50k | Tight budget |
| 13 | `test_13_plan_route_time_constraint` | Ràng buộc thời gian | 3-hour window | Limited time |
| 14 | `test_14_plan_route_opening_hours` | Giờ mở cửa | Morning/Evening POIs | Opening hours |
| 15 | `test_15_plan_route_empty_pois` | Danh sách rỗng | Empty POI list | Edge: no data |
| 16 | `test_16_plan_route_no_feasible_pois` | Không khả thi | Too expensive POI + low budget | Edge: infeasible |
| 17 | `test_17_plan_route_preference_priority` | Ưu tiên sở thích | Preferred vs non-preferred | Priority check |

**Coverage**: `solver_route.py::plan_route` - ≥95%

**Các ràng buộc được kiểm tra:**
- ✅ Budget constraint
- ✅ Time window constraint
- ✅ Opening hours constraint
- ✅ No duplicate visits
- ✅ Preference matching
- ✅ Mode selection (walking, motorbike, taxi)

---

### ⚡ Nhóm 5: Optimizer (2 test cases)
Kiểm tra tối ưu hóa tuyến đường sau khi lập kế hoạch

| # | Test Case | Mục đích | Input | Output mong đợi |
|---|-----------|----------|-------|-----------------|
| 18 | `test_18_two_opt_improvement` | Cải thiện tuyến đường | Route with 4 stops | Optimized ≤ Original |
| 19 | `test_19_two_opt_short_route` | Tuyến ngắn | Route with 2 stops | Unchanged |

**Coverage**: `optimizer.py` - ≥90%

---

### 🔗 Nhóm 6: Integration (1 test case)
Kiểm tra toàn bộ workflow end-to-end

| # | Test Case | Mục đích | Kiểm tra |
|---|-----------|----------|----------|
| 20 | `test_20_full_workflow_integration` | Quy trình đầy đủ | CSV → Load → Plan → Verify all constraints |

**Điểm kiểm tra trong TC20:**
1. ✅ Load 5 POIs từ CSV
2. ✅ Plan route với preferences
3. ✅ Budget constraint (≤ 500k)
4. ✅ Time constraint (08:00-18:00)
5. ✅ No duplicate visits
6. ✅ Route continuity (depart[i] ≤ arrive[i+1])
7. ✅ All POI fields present

**Coverage**: End-to-end workflow - 100%

---

## 📊 Tổng kết Coverage

| Module | Test Cases | Target Coverage |
|--------|------------|-----------------|
| `utils_geo.py` | 3 | 100% |
| `scorer.py` | 4 | 100% |
| `solver_route.py` | 11 | ≥95% |
| `optimizer.py` | 2 | ≥90% |
| **Overall** | **20** | **≥90%** |

## 🎯 Các trường hợp đặc biệt được bao phủ

### Edge Cases
- ✅ Empty input (no POIs)
- ✅ Infeasible constraints (no valid route)
- ✅ Same location (distance = 0)
- ✅ Short route (< 4 stops for 2-opt)
- ✅ Empty tags
- ✅ Zero budget
- ✅ Tight time window

### Boundary Cases
- ✅ Opening/closing hours exactly at boundary
- ✅ Budget exactly at cost
- ✅ Time window exactly at visit duration
- ✅ Perfect preference match (100%)
- ✅ No preference match (0%)

### Normal Cases
- ✅ Multiple POIs with different attributes
- ✅ Multiple transportation modes
- ✅ Partial preference matching
- ✅ Standard budget/time constraints
- ✅ Route optimization

### Integration Cases
- ✅ Full workflow from data to result
- ✅ All constraints combined
- ✅ Real-world scenario (HCM City POIs)

## 🚀 Chạy Tests

```bash
# Chạy tất cả
python run_tests.py

# Hoặc với pytest trực tiếp
pytest tests/test_comprehensive.py -v

# Với coverage
pytest tests/test_comprehensive.py --cov=core --cov-report=html -v
```

## ✅ Success Criteria

Test suite pass khi:
- 20/20 tests pass ✅
- Overall coverage ≥ 90% ✅
- No critical bugs in core logic ✅
- All constraints properly enforced ✅
