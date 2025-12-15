import math
from datetime import datetime, timedelta


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.asin(math.sqrt(a))


def suggest_places(current_loc, current_time, end_time, budget_left, K, prefs, pois):
    results = []

    for poi in pois:
        # Filter by time
        if poi["close_hour"] <= current_time.hour:
            continue

        # Filter by budget
        if poi["cost"] > budget_left:
            continue

        # Distance calculation
        dist = haversine(current_loc[0], current_loc[1], poi["lat"], poi["lon"])
        travel_time_hours = dist / 4  # walking speed 4km/h
        arrival_time = current_time + timedelta(hours=travel_time_hours)

        if arrival_time > end_time:
            continue

        # Score components
        score_distance = 1 / (1 + dist)
        score_rating = poi["rating"] / 5
        score_pref = prefs.get(poi["category"], 0)

        score = 0.4 * score_distance + 0.3 * score_rating + 0.3 * score_pref

        results.append({
            "score": score,
            "dist": dist,
            "poi": poi,
            "travel_time_hours": travel_time_hours
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:K]
