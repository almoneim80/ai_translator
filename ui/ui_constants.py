import os

# -------------------- Base Paths --------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(BASE_DIR, "../resources/icons")
WINDOW_ICON_PATH = os.path.join(RESOURCES_DIR, "icon.png")
TRAY_ICON_PATH = os.path.join(RESOURCES_DIR, "icon.png")
COPY_ICON_PATH = os.path.join(RESOURCES_DIR, "copy-solid-full.svg")
HIDE_ICON_PATH = os.path.join(RESOURCES_DIR, "hide.svg")
More_ICON_PATH = os.path.join(RESOURCES_DIR, "ellipsis.svg")

# -------------------- Window Settings --------------------
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 200
APP_TITLE = "Baligh"
SETTINGS_ICON_WIDTH = 24
SETTINGS_ICON_HEIGH = 24
TRANSLATOR_WINDOW_FULL_WIDTH = 400
TRANSLATOR_WINDOW_FULL_HEIGHT = 300
TRANSLATOR_WINDOW_VISIBLE_WIDTH = 20
WINDOW_TOP_MARGIN = 20
WINDOW_COLLAPSE_DELAY_MS = 500
TRANSLATION_COLLAPSE_DELAY_MS = 10000
WINDOW_EDGE_MARGIN = 30
RIGHT_MARGIN = 5
LAST_TRANSLATED_TEXT = ""
HOVER_DEFAULT = False
CLIPBOARD_ENABLED_DEFAULT = True

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
