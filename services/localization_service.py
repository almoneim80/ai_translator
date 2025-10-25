import json
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCALIZATION_FILE = os.path.join(BASE_DIR, "../Localization/en.json")


def load_localization(file_path=LOCALIZATION_FILE):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading localization: {e}")
        return {}


LOCALIZATION = load_localization()


def get_text(key: str, default: str = "") -> str:
    """
    Return the localized string for the given key.
    """
    return LOCALIZATION.get(key, default)