import requests, time
# Chức năng:
# +Gọi API Overpass (OpenStreetMap)
# +Query POIs theo bounding box
# +Lọc theo categories
# +Trả list POIs

#Đây là module lấy dữ liệu thật từ OSM.

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

OSM_FILTERS = [
    '["tourism"]',
    '["amenity"]',
    '["shop"]',
    '["leisure"]',
    '["historic"]'
]

def fetch_osm_pois(lat, lon, radius=5000):
    query = f"""
    [out:json][timeout:25];
    (
        {"".join([f"node {f} (around:{radius},{lat},{lon});" for f in OSM_FILTERS])}
    );
    out body;
    """
    for retry in range(3):
        try:
            res = requests.get(OVERPASS_URL, params={"data": query}, timeout=30)
            res.raise_for_status()
            return res.json().get("elements", [])
        except:
            time.sleep(2)
    return []
