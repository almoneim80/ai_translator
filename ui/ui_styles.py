from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt


# ---------------- Window ----------------
def apply_window_style(window):
    window.setStyleSheet("""
        border-radius: 15px;
        color: #333333;
        font-family: 'Segoe UI', Tahoma, sans-serif;
        font-size: 14px;
        background: transparent;
    """)
    shadow = QGraphicsDropShadowEffect()
    shadow.setBlurRadius(25)
    shadow.setXOffset(0)
    shadow.setYOffset(5)
    shadow.setColor(Qt.gray)


# ---------------- Translation Box ----------------
TRANSLATION_BOX_STYLE = """
    background-color: #2d3748;
    color: #e2e8f0;
    border-radius: 8px;
    padding: 10px;
    font-family: 'Segoe UI', Tahoma, sans-serif;
    font-size: 14px;
"""

# ---------------- Card ----------------
CARD_STYLE = """
    background-color: #2d3748;
    border-radius: 10px;
    padding: 8px;
"""

# ---------------- Button ----------------
BUTTON_STYLE = """
    QPushButton {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
    }
    QPushButton:hover {
        background-color: rgba(255, 255, 255, 0.25);
    }
"""

# ---------------- Settings Button ----------------
BUTTON_STYLE = """
    QPushButton {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
    }
    QPushButton:hover {
        background-color: rgba(255, 255, 255, 0.25);
    }
"""

# ---------------- Settings Menu ----------------
SETTINGS_MENU_STYLE = """
        QMenu {
            background-color: rgba(45, 55, 72, 0.95);
            color: #f1f5f9;
            border-radius: 12px;
            padding: 4px;
            margin: 0px;
            border: 1px solid #4b5563;
        }
        QMenu::item {
            padding: 6px 16px;
            margin: 0px;
        }
        QMenu::item:selected {
            background-color: #2563eb;
            border-radius: 12px;
            color: #ffffff;
        }
        QMenu::separator {
            height: 1px;
            background: #374151;
            margin: 4px 0px;
        }
"""

# ---------------- Settings Menu ----------------
SETTINGS_BUTTON_STYLE = f"""
    QToolButton {{
        border-radius: 8px;
        background-color: rgba(255, 255, 255, 0.1);
        padding: 4px;             
    }}
    QToolButton:hover {{
        background-color: rgba(255, 255, 255, 0.25);
    }}
    QToolButton::menu-indicator {{
        image: none;
    }}
"""
