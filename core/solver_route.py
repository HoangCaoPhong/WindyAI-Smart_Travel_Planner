# core/solver_route.py
import pandas as pd
from datetime import datetime, timedelta
from core.utils_geo import travel_info
from core.scorer import score_candidate
from core.config import DEFAULT_BUDGET, DEFAULT_TIME_WINDOW, DEFAULT_START

def load_pois(csv_path):
    """
    Load POIs from csv and normalize fields.
    Required columns: id,name,lat,lon,open_hour,close_hour,visit_duration_min,entry_fee,rating,tags
    tags stored as "a;b;c" in CSV -> becomes ['a','b','c']
    Also fill alias 'visit_duration' for backward compatibility.
    """
    df = pd.read_csv(csv_path)
    pois = df.to_dict("records")
    for p in pois:
        tags = p.get("tags", "")
        p["tags"] = tags.split(";") if isinstance(tags, str) and tags != "" else []
        # alias
        p["visit_duration"] = p.get("visit_duration_min", p.get("visit_duration", 30))
        # ensure numeric types
        p["lat"] = float(p["lat"])
        p["lon"] = float(p["lon"])
        p["open_hour"] = int(p.get("open_hour", 0))
        p["close_hour"] = int(p.get("close_hour", 23))
        p["entry_fee"] = float(p.get("entry_fee", 0.0))
        p["rating"] = float(p.get("rating", 0.0))
    return pois

def plan_route(pois, user_prefs=None, start_loc=DEFAULT_START,
               time_window=DEFAULT_TIME_WINDOW, budget=DEFAULT_BUDGET):
    """
    Greedy + lookahead(1) route planner.
    Returns list of route steps with arrival/depart times and costs.
    """
    user_prefs = user_prefs or []
    start_time = datetime.strptime(time_window[0], "%Y-%m-%d %H:%M")
    end_time = datetime.strptime(time_window[1], "%Y-%m-%d %H:%M")
    current_time = start_time
    current_loc = start_loc
    budget_left = budget
    visited = set()
    route = []

    while True:
        candidates = []
        for poi in pois:
            if poi["id"] in visited:
                continue

            for mode in ["walking", "motorbike", "taxi"]:
                _, travel_min, travel_cost = travel_info(current_loc, (poi["lat"], poi["lon"]), mode)
                arrive = current_time + timedelta(minutes=travel_min)
                finish = arrive + timedelta(minutes=float(poi.get("visit_duration_min", poi["visit_duration"])))

                # constraints: open/close hour, overall end_time, budget
                # Note: compare hours simply (assumes same-day)
                if (arrive.hour < poi["open_hour"] or finish.hour > poi["close_hour"] or finish > end_time):
                    continue

                if budget_left < (travel_cost + poi.get("entry_fee", 0.0)):
                    continue

                score = score_candidate(poi, travel_min, travel_cost, user_prefs)
                candidates.append((score, poi, mode, arrive, finish, travel_cost))

        if not candidates:
            break

        # choose best candidate (lowest score)
        candidates.sort(key=lambda x: x[0])
        best = candidates[0]
        _, best_poi, best_mode, arrive, finish, cost = best

        route.append({
            "id": best_poi["id"],
            "name": best_poi["name"],
            "mode": best_mode,
            "arrive_time": arrive,
            "depart_time": finish,
            "travel_cost": cost,
            "entry_fee": best_poi["entry_fee"]
        })

        visited.add(best_poi["id"])
        budget_left -= (best_poi["entry_fee"] + cost)
        current_time = finish
        current_loc = (best_poi["lat"], best_poi["lon"])

    return route
