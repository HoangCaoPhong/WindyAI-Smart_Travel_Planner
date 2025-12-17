INPUT:
    current_loc (lat, lon)
    current_time (datetime)
    end_time (datetime)
    budget_left (float)
    K (int)
    prefs (dict: category → weight)
    POIs (list of objects)

OUTPUT:
    top_K_suggestions

ALGO:
    candidates = []

    for poi in POIs:
        if poi.closing_hour < current_time: continue
        if poi.cost > budget_left: continue
        
        dist = haversine(current_loc, poi.loc)
        travel_time = dist / walking_speed

        if current_time + travel_time > end_time: continue

        score_distance = normalize(1 / (dist + 1))
        score_rating   = normalize(poi.rating)
        score_pref     = prefs.get(poi.category, 0)

        score = (
            0.4 * score_distance +
            0.3 * score_rating +
            0.3 * score_pref
        )

        candidates.append((score, poi))

    sort candidates by score descending

    return top K POIs
ư