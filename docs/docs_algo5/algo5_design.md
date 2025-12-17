# Algo5 – Place Suggestion Engine (Location-based Recommendation)

## 1. Objective
Gợi ý top-K địa điểm (POIs) phù hợp cho người dùng dựa trên:
- vị trí hiện tại  
- thời gian còn lại  
- ngân sách còn lại  
- sở thích POI  
- khoảng cách  
- rating  
- thời gian mở cửa  

## 2. Inputs
- `current_loc` = (lat, lon)
- `current_time`
- `end_time`
- `budget_left`
- `K` — số POI muốn gợi ý
- `user_pref` = {category → weight}
- `POI dataset`

## 3. Constraints
- Không vượt quá thời gian đóng cửa
- Không vượt quá budget
- Ưu tiên POI gần, rating cao, hợp sở thích

## 4. Output
Danh sách top K POI + metadata:
- tên  
- loại  
- rating  
- estimated travel time  
- estimated cost  

## 5. Scoring Model
### Score = W1 * distance_score  
          + W2 * rating_score  
          + W3 * preference_score  
          + W4 * time_fit_score

W1…W4 lấy từ config.

---

## 6. Steps
1. Lọc POI theo open hours  
2. Tính distance + travel time  
3. Tính score theo công thức  
4. Sắp xếp giảm dần theo score  
5. Chọn top K  
