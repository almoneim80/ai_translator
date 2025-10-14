import json
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(base_dir, "config.json")


def load_config():
    """
    Load configuration settings from the 'config.json' file.

    This function locates the configuration file located two levels above
    the current file's directory, reads its contents, and returns them
    as a Python dictionary.

    Returns:
        dict: A dictionary containing the configuration settings.

    Raises:
        FileNotFoundError: If the 'config.json' file does not exist.
        json.JSONDecodeError: If the file content is not valid JSON.
        UnicodeDecodeError: If the file encoding is invalid.
    """
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)
