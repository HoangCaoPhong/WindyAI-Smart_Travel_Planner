from fastapi import FastAPI
from core.solver_route import load_pois, plan_route

app = FastAPI(title="Smart Travel AI")

@app.get("/")
def home():
    return {
        "message": "Smart Travel AI API running — visit /docs",
        "docs": "/docs"
    }

@app.post("/plan")
def plan(input_data: dict):
    pois = load_pois("data/pois_hcm_large.csv")  # dataset lớn
    route = plan_route(
        pois,
        input_data.get("preferences", []),
        tuple(input_data.get("start_location")),
        (input_data["start_time"], input_data["end_time"]),
        input_data.get("budget", 1_000_000),
    )
    return {
        "total_stops": len(route),
        "itinerary": [
            {
                "name": r["name"],
                "arrive": r["arrive_time"].strftime("%H:%M"),
                "depart": r["depart_time"].strftime("%H:%M"),
                "mode": r["mode"],
                "cost": int(r["travel_cost"]),
                "entry_fee": int(r["entry_fee"])
            } for r in route
        ]
    }
