#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để lấy POIs từ OpenStreetMap (Overpass API)
Lấy các điểm du lịch, nhà hàng, công viên, bảo tàng, v.v. ở TP.HCM
"""

import requests
import pandas as pd
import time
import json

# Overpass API endpoint
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# Định nghĩa query cho TP.HCM (bbox: south, west, north, east)
# TPHCM: roughly 10.5-11.0 lat, 106.4-107.0 lon
BBOX = "10.5,106.4,11.0,107.0"

def query_overpass(query):
    """Gửi query đến Overpass API"""
    try:
        response = requests.post(OVERPASS_URL, data={"data": query}, timeout=60)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Lỗi query Overpass: {e}")
        return None

def get_pois_by_category(category_query, category_name, max_results=100):
    """
    Lấy POIs theo từng category
    """
    print(f"\n🔍 Đang tìm {category_name}...")
    
    query = f"""
    [out:json][timeout:60];
    (
      {category_query}
    );
    out center {max_results};
    """
    
    data = query_overpass(query)
    if not data or "elements" not in data:
        return []
    
    pois = []
    for element in data["elements"]:
        # Lấy tọa độ
        if "lat" in element and "lon" in element:
            lat, lon = element["lat"], element["lon"]
        elif "center" in element:
            lat, lon = element["center"]["lat"], element["center"]["lon"]
        else:
            continue
        
        # Lấy thông tin
        tags = element.get("tags", {})
        name = tags.get("name", tags.get("name:vi", tags.get("name:en", "Unknown")))
        
        # Lọc những POI không có tên hoặc tên quá ngắn
        if not name or len(name) < 3 or name == "Unknown":
            continue
        
        # Rating mặc định (OSM không có rating)
        rating = 4.0 + (hash(name) % 10) / 10  # Random 4.0-4.9
        
        # Visit duration theo loại
        visit_duration = 60  # mặc định 1 giờ
        if "museum" in category_name.lower():
            visit_duration = 90
        elif "park" in category_name.lower():
            visit_duration = 45
        elif "restaurant" in category_name.lower() or "food" in category_name.lower():
            visit_duration = 90
        elif "shopping" in category_name.lower():
            visit_duration = 120
        
        # Entry fee
        entry_fee = 0
        if tags.get("fee") == "yes" or "museum" in category_name.lower():
            entry_fee = 30000 + (hash(name) % 5) * 10000  # 30k-80k
        
        # Opening hours
        opening_hours = tags.get("opening_hours", "")
        open_hour = 8
        close_hour = 18
        
        if "24/7" in opening_hours:
            open_hour = 0
            close_hour = 23
        elif "restaurant" in category_name.lower() or "food" in category_name.lower():
            open_hour = 10
            close_hour = 22
        elif "nightlife" in category_name.lower():
            open_hour = 18
            close_hour = 2
        
        poi = {
            "name": name,
            "lat": lat,
            "lon": lon,
            "tags": category_name,
            "rating": round(rating, 1),
            "visit_duration_min": visit_duration,
            "entry_fee": entry_fee,
            "open_hour": open_hour,
            "close_hour": close_hour,
        }
        
        pois.append(poi)
    
    print(f"  ✓ Tìm thấy {len(pois)} {category_name}")
    return pois

def main():
    print("="*70)
    print("   🗺️  LẤY DỮ LIỆU POIs TỪ OPENSTREETMAP (TP.HCM)")
    print("="*70)
    
    all_pois = []
    
    # Định nghĩa các categories
    categories = [
        # Museums & Culture
        {
            "query": f'node["tourism"="museum"]({BBOX});',
            "name": "history;museum;culture",
            "max": 30
        },
        # Landmarks & Monuments
        {
            "query": f'node["historic"]({BBOX});',
            "name": "history;landmark",
            "max": 30
        },
        # Parks & Nature
        {
            "query": f'node["leisure"="park"]({BBOX});',
            "name": "park;nature;relaxation",
            "max": 30
        },
        # Shopping
        {
            "query": f'node["shop"="mall"]({BBOX});',
            "name": "shopping;modern",
            "max": 20
        },
        # Restaurants & Food
        {
            "query": f'node["amenity"="restaurant"]({BBOX});',
            "name": "food;restaurant",
            "max": 50
        },
        # Entertainment
        {
            "query": f'node["tourism"="attraction"]({BBOX});',
            "name": "entertainment;attraction",
            "max": 30
        },
        # Viewpoints
        {
            "query": f'node["tourism"="viewpoint"]({BBOX});',
            "name": "viewpoint;modern",
            "max": 15
        },
        # Religious
        {
            "query": f'node["amenity"="place_of_worship"]({BBOX});',
            "name": "religious;culture",
            "max": 25
        },
        # Markets
        {
            "query": f'node["amenity"="marketplace"]({BBOX});',
            "name": "shopping;food;market",
            "max": 20
        },
    ]
    
    # Lấy POIs từng category
    for i, cat in enumerate(categories, 1):
        print(f"\n[{i}/{len(categories)}]")
        pois = get_pois_by_category(cat["query"], cat["name"], cat["max"])
        all_pois.extend(pois)
        time.sleep(2)  # Rate limiting
    
    # Loại bỏ duplicate (theo tên)
    print(f"\n📊 Tổng số POIs: {len(all_pois)}")
    df = pd.DataFrame(all_pois)
    
    # Loại bỏ duplicate theo tên
    df = df.drop_duplicates(subset=["name"], keep="first")
    print(f"📊 Sau khi loại bỏ duplicate: {len(df)}")
    
    # Thêm ID
    df.insert(0, "id", range(1, len(df) + 1))
    
    # Sắp xếp theo rating và tên
    df = df.sort_values(["rating", "name"], ascending=[False, True])
    df["id"] = range(1, len(df) + 1)
    
    # Lưu file
    output_file = "data/pois_hcm_extended.csv"
    df.to_csv(output_file, index=False, encoding="utf-8")
    
    print(f"\n{'='*70}")
    print(f"✅ ĐÃ LƯU {len(df)} POIs VÀO: {output_file}")
    print(f"{'='*70}")
    
    # Hiển thị thống kê
    print("\n📊 THỐNG KÊ THEO CATEGORY:")
    for tag_group in df["tags"].unique():
        count = len(df[df["tags"] == tag_group])
        print(f"  • {tag_group}: {count} POIs")
    
    # Hiển thị 10 POI đầu tiên
    print("\n📍 TOP 10 POIs (theo rating):")
    for i, row in df.head(10).iterrows():
        print(f"  {row['id']}. {row['name']} - {row['rating']}⭐ ({row['tags']})")
    
    print(f"\n💡 Để sử dụng, thay đổi trong solver_route.py:")
    print(f"   csv_path = 'data/pois_hcm_extended.csv'")

if __name__ == "__main__":
    main()
