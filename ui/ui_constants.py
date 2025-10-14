import os

# -------------------- Base Paths --------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(BASE_DIR, "../resources")
ICON_PATH = os.path.join(RESOURCES_DIR, "icon.png")

# -------------------- Window Settings --------------------
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 200
APP_TITLE = "Baligh"

# -------------------- Language Mapping --------------------
LANGUAGE_MAP = {
    "Arabic": "arb_Arab",
    "French": "fra_Latn",
    "Spanish": "spa_Latn",
    "English": "eng_Latn"
}

# -------------------- Style / Shadow Defaults --------------------
SHADOW_BLUR_RADIUS = 25
SHADOW_X_OFFSET = 0
SHADOW_Y_OFFSET = 5
SHADOW_COLOR = "gray"
