# core/algo6_chatbot/knowledge_base.py

import pandas as pd
from typing import Dict, Optional
import requests
import os

try:
    from core.algo1.solver_route import load_pois, plan_route
except ImportError:
    def load_pois(csv_path="data/pois.csv", **kwargs):
        df = pd.read_csv(csv_path)
        return df.to_dict("records")

    def plan_route(*args, **kwargs):
        return []

OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY", "")

def get_weather(lat: float, lon: float) -> Optional[Dict]:
    if not OPENWEATHER_KEY:
        return None
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_KEY}&units=metric&lang=vi"
    try:
        res = requests.get(url, timeout=6)
        return res.json() if res.status_code == 200 else None
    except:
        return None
