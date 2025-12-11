# core/algo6_chatbot/response_generator.py

def format_pois(pois, n=5):
    if not pois:
        return "Không tìm thấy địa điểm phù hợp."
    lines = []
    for p in pois[:n]:
        name = p.get("name", "Unknown")
        fee = p.get("entry_fee", "0")
        rating = p.get("rating", "N/A")
        lines.append(f"- {name} | Vé: {fee} VND | Rating: {rating}")
    return "Gợi ý địa điểm:\n" + "\n".join(lines)

def format_weather(w):
    if not w:
        return "Không có dữ liệu thời tiết."
    desc = w["weather"][0]["description"]
    temp = w["main"]["temp"]
    wind = w["wind"]["speed"]
    return f"Thời tiết: {desc}, {temp}°C, gió {wind} m/s."

def format_route(route):
    if not route:
        return "Không tạo được lộ trình."
    lines = []
    for r in route:
        lines.append(f"- {r['name']} ({r['arrive_time'].strftime('%H:%M')} → {r['depart_time'].strftime('%H:%M')})")
    return "Lộ trình đề xuất:\n" + "\n".join(lines)
