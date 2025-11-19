"""Utility functions for WindyAI app"""
from datetime import time

def time_to_minutes(t: time) -> int:
    """Convert time object to minutes since midnight"""
    return t.hour * 60 + t.minute

def minutes_to_str(m: int) -> str:
    """Convert minutes to HH:MM string format"""
    h = m // 60
    mm = m % 60
    return f"{h:02d}:{mm:02d}"
