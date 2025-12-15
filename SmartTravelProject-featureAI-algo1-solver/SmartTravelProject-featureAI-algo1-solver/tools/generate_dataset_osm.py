# tools/generate_dataset_osm.py
# Chức năng:
# + Chia TP.HCM thành grid
# + Gọi OSM API từng ô
# + Ghép dữ liệu → tạo CSV hoàn chỉnh
# Tạo file:
# + pois_hcm_large.csv (1000–3000 POIs)
import os
import sys
import pandas as pd

# Thêm thư mục gốc vào PYTHONPATH
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from tools.osm_fetcher import fetch_osm_pois

# Trung tâm TP.HCM
CENTER = (10.7769, 106.7006)

# Chia lưới 5x5 để bao phủ toàn TP.HCM
LAT_OFFSETS = [-0.12, -0.06, 0, 0.06, 0.12]
LON_OFFSETS = [-0.12, -0.06, 0, 0.06, 0.12]

RADIUS = 3000   # mỗi ô quét bán kính 3km

rows = []
seen = set()
id_counter = 1

for dlat in LAT_OFFSETS:
    for dlon in LON_OFFSETS:
        lat = CENTER[0] + dlat
        lon = CENTER[1] + dlon

        print(f"Fetching POIs at cell: {lat}, {lon}")
        elements = fetch_osm_pois(lat, lon, RADIUS)

        for e in elements:
            uid = e.get("id")
            if uid in seen:
                continue
            seen.add(uid)

            tags = e.get("tags", {})
            name = tags.get("name")
            if not name:
                continue

            rows.append({
                "id": id_counter,
                "name": name,
                "lat": e["lat"],
                "lon": e["lon"],
                "open_hour": 6,
                "close_hour": 22,
                "visit_duration_min": 30,
                "entry_fee": 0,
                "rating": 4.0,
                "tags": ";".join(tags.keys())
            })
            id_counter += 1

df = pd.DataFrame(rows)
os.makedirs("data", exist_ok=True)
df.to_csv("data/pois_hcm_large.csv", index=False)
print("Generated POIs:", len(df))
