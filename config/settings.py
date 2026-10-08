"""
Configuración general de la aplicación
"""
APP_NAME = "SHIFTMODE"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Diego Matute"

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 840
WINDOW_MIN_WIDTH = 980
WINDOW_MIN_HEIGHT = 680

DEFAULT_THEME = "light"
SHIFT_DURATION_HOURS = 8
LUNCH_DURATION_MINUTES = 60

COLORS = {
    "light": {
        "bg": "#FFFFFF",
        "fg": "#121212",
        "primary": "#0066FF",
        "secondary": "#F3F5F8",
        "accent": "#FF6B57",
        "border": "#E7EAF0",
        "text": "#121212",
        "text_secondary": "#7A7F8A",
    },
    "dark": {
        "bg": "#121212",
        "fg": "#F3F5F8",
        "primary": "#4DA3FF",
        "secondary": "#1F1F1F",
        "accent": "#FF7A5C",
        "border": "#2D2D2D",
        "text": "#F3F5F8",
        "text_secondary": "#A2A7B3",
    }
}

CHART_COLORS = ["#0066FF", "#FF6B57", "#2EB67D", "#F4B942", "#8E6BE8", "#7CC6FE"]
