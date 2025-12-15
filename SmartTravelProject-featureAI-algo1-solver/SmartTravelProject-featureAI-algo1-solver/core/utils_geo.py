# core/utils_geo.py
# Chức năng:
# + Tính khoảng cách giữa hai toạ độ (Haversine)
# + Tính thời gian và chi phí di chuyển (travel_info)
# -> Thuật toán sử dụng file này cho mỗi lần check POI.
import math
from core.config import SPEEDS_KMH, COST_PER_KM

def haversine_km(a, b):
    """Return great-circle distance (km) between two (lat, lon) tuples."""
    R = 6371.0
    lat1, lon1 = map(math.radians, a)
    lat2, lon2 = map(math.radians, b)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    h = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(h))

def travel_info(a, b, mode="motorbike"):
    """
    Return tuple (distance_km, time_min, cost_vnd) for travel between a and b.
    a, b: (lat, lon)
    mode: "walking" | "motorbike" | "taxi"
    """
    d = haversine_km(a, b)
    speed = SPEEDS_KMH.get(mode, 25)
    time_min = (d / speed) * 60.0
    cost = d * COST_PER_KM.get(mode, 0.0)
    return d, time_min, cost
