# core/algo6_chatbot/intent_classifier.py

INTENT_KEYWORDS = {
    "poi_search": ["địa điểm", "đi đâu", "chơi gì", "gợi ý", "tham quan", "nên đi"],
    "price": ["giá vé", "giá", "bao nhiêu", "phí vào", "vé"],
    "weather": ["thời tiết", "mưa", "nắng", "nhiệt độ", "weather"],
    "route": ["lộ trình", "tuyến đường", "tối ưu", "đi đường nào", "plan"],
    "smalltalk": ["xin chào", "chào", "hello", "hi", "cảm ơn"]
}

def classify_intent(query: str):
    q = query.lower()
    scores = {k: 0 for k in INTENT_KEYWORDS}

    for intent, words in INTENT_KEYWORDS.items():
        for w in words:
            if w in q:
                scores[intent] += 1

    top = max(scores, key=lambda k: scores[k])
    if scores[top] == 0:
        return "llm"

    return top
