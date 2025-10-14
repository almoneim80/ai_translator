import os
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from .ui_styles import apply_window_style
from baligh.ui.ui_constants import ICON_PATH, WINDOW_WIDTH, WINDOW_HEIGHT, APP_TITLE


def setup_window(window):
    """
    Configure the main translator window's functional setup
    and apply styling from ui_styles.

    Args:
        window (QWidget): The window instance to configure.
    """

    # Functional setup using constants
    window.setWindowTitle(APP_TITLE)
    window.setWindowIcon(QIcon(ICON_PATH))
    window.setAttribute(Qt.WA_TranslucentBackground)
    window.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    window.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

    # Apply centralized styling (colors, shadow, font)
    apply_window_style(window)
