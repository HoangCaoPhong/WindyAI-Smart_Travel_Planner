import json
from datetime import datetime
from core.algo5.algo5_suggester import suggest_places

# Load dataset
with open("data/algo5/poi_sample.json", "r", encoding="utf-8") as f:
    pois = json.load(f)

# Input cho demo
current_loc = (10.762622, 106.660172)     # Bản đồ HCMUS
current_time = datetime(2025, 1, 1, 14, 0)  # 14:00
end_time = datetime(2025, 1, 1, 18, 0)      # 18:00
budget_left = 100
K = 3

prefs = {
    "cafe": 0.9,
    "park": 0.7,
    "museum": 0.4,
}

# Run algorithm
results = suggest_places(
    current_loc=current_loc,
    current_time=current_time,
    end_time=end_time,
    budget_left=budget_left,
    K=K,
    prefs=prefs,
    pois=pois,
)

# Print output
print("\n===== TOP GỢI Ý ĐỊA ĐIỂM =====\n")
for r in results:
    poi = r["poi"]
    print(f"- {poi['name']} ({poi['category']})")
    print(f"  Rating: {poi['rating']}")
    print(f"  Distance: {r['dist']:.2f} km")
    print(f"  Score: {r['score']:.3f}")
    print("")
