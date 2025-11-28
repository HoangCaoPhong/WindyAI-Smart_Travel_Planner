"""Utility functions for WindyAI app"""
from datetime import time
import base64
import os

def time_to_minutes(t: time) -> int:
    """Convert time object to minutes since midnight"""
    return t.hour * 60 + t.minute

def minutes_to_str(m: int) -> str:
    """Convert minutes to HH:MM string format"""
    h = m // 60
    mm = m % 60
    return f"{h:02d}:{mm:02d}"

def get_image_base64(image_path):
    """Chuyển đổi ảnh sang base64 để hiển thị trong HTML."""
    if not os.path.exists(image_path):
        return ""
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')
