# core/algo6_chatbot/chatbot_engine.py

import os
import requests
from .intent_classifier import classify_intent
from .knowledge_base import load_pois, get_weather, plan_route
from .response_generator import format_pois, format_weather, format_route

# ======== LLM API CONFIG ===========
GROQ_KEY = os.getenv("GROQ_API_KEY", "")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

# ======== LLM CONNECTORS ===========

def call_groq(query: str):
    if not GROQ_KEY:
        return None
    try:
        from groq import Groq
        client = Groq(api_key=GROQ_KEY)
        res = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": query}],
            max_tokens=300,
            temperature=0.7,
        )
        return res.choices[0].message.content
    except:
        return None

def call_ollama(query: str):
    try:
        body = {"model": "llama3", "prompt": query, "stream": False}
        r = requests.post(f"{OLLAMA_URL}/api/generate", json=body, timeout=10)
        j = r.json()
        return j.get("response")
    except:
        return None

def ask_llm(query: str):
    out = call_groq(query)
    if out:
        return out

    out = call_ollama(query)
    if out:
        return out

    return "Hiện tại mình chưa kết nối được mô hình AI. Bạn hãy hỏi về địa điểm, giá vé hoặc thời tiết nhé."

# ============ MAIN CHATBOT LOGIC ===============

def chatbot(query: str):
    intent = classify_intent(query)
    q = query.lower()

    # POI search
    if intent == "poi_search":
        pois = load_pois()
        matches = []
        for p in pois:
            name = p["name"].lower()
            if any(w in q for w in name.split()):
                matches.append(p)
        if not matches:
            matches = sorted(pois, key=lambda x: x.get("rating", 0), reverse=True)
        return {"answer": format_pois(matches)}

    # Price
    if intent == "price":
        pois = load_pois()
        for p in pois:
            if p["name"].lower() in q:
                return {"answer": f"Giá vé {p['name']} hiện tại: {p.get('entry_fee','không rõ')} VND."}
        return {"answer": "Không tìm thấy địa điểm. Bạn nhập tên đầy đủ nhé."}

    # Weather
    if intent == "weather":
        pois = load_pois()
        for p in pois:
            if p["name"].lower() in q:
                w = get_weather(p["lat"], p["lon"])
                return {"answer": format_weather(w)}
        return {"answer": ask_llm(query)}

    # Route planner
    if intent == "route":
        pois = load_pois()
        route = plan_route(pois, user_prefs=[], time_window=("08:00", "18:00"))
        return {"answer": format_route(route)}

    # Smalltalk or LLM fallback
    return {"answer": ask_llm(query)}
