from core.algo1 import load_pois

pois = load_pois('data/pois_hcm_extended.csv')
print(f'✓ Loaded {len(pois)} POIs')
print(f'  - Museums: {len([p for p in pois if "museum" in str(p.get("tags", ""))])}')
print(f'  - Restaurants: {len([p for p in pois if "restaurant" in str(p.get("tags", ""))])}')
print(f'  - Parks: {len([p for p in pois if "park" in str(p.get("tags", ""))])}')
print(f'  - Religious: {len([p for p in pois if "religious" in str(p.get("tags", ""))])}')
print(f'\nSample POIs:')
for i, poi in enumerate(pois[:5], 1):
    print(f'  {i}. {poi["name"]} - {poi["rating"]}⭐')
