"""
Theme Manager for MindEase.
Automatically switches between Light and Dark themes.
"""

from datetime import datetime


LIGHT_THEME = {
    "background": "#EAF6FF",
    "card": "#FFFFFF",
    "primary": "#6CB4EE",
    "accent": "#A8E6CF",
    "text": "#1F2937",
    "secondary_text": "#6B7280",
}

DARK_THEME = {
    "background": "#0F172A",
    "card": "#1E293B",
    "primary": "#8B5CF6",
    "accent": "#C4B5FD",
    "text": "#F8FAFC",
    "secondary_text": "#CBD5E1",
}


def get_theme(mode: str = "Auto") -> dict:
    """
    Returns the current theme.
    mode:
        Auto
        Light
        Dark
    """

    if mode == "Light":
        return LIGHT_THEME

    if mode == "Dark":
        return DARK_THEME

    current_hour = datetime.now().hour

    if 6 <= current_hour < 18:
        return LIGHT_THEME

    return DARK_THEME