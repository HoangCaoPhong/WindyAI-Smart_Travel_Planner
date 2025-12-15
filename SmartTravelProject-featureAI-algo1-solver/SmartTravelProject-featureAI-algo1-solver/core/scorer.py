# core/scorer.py
#Trả về score -> dùng để rank POI.
from core.config import ALPHA, BETA, GAMMA, DELTA, EPSILON

def preference_score(tags, user_prefs):
    """
    tags: list or set of tag strings for POI
    user_prefs: list or set
    return: [0..1] how well POI matches user's preferences
    """
    if not tags or not user_prefs:
        return 0.0
    tags_set = set(tags)
    prefs_set = set(user_prefs)
    return len(tags_set & prefs_set) / len(prefs_set)

def score_candidate(poi, travel_min, travel_cost, user_prefs):
    """
    Lower score = better candidate (we will sort ascending).
    poi: dict contains 'rating' and 'visit_duration_min'
    """
    pref = preference_score(poi.get("tags", []), user_prefs)
    rating = float(poi.get("rating", 0.0))
    visit_duration = float(poi.get("visit_duration_min", 30))
    # score components: time, visit, cost penalize; rating and pref reduce score
    score = (ALPHA * travel_min
             + BETA * visit_duration
             + GAMMA * travel_cost
             - DELTA * rating
             - EPSILON * pref)
    return score
