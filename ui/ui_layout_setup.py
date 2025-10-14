from PyQt5.QtWidgets import (
    QVBoxLayout, QTextEdit, QWidget, QPushButton, QHBoxLayout,
    QAction, QMenu, QToolButton
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import os
from baligh.ui.ui_styles import TRANSLATION_BOX_STYLE, CARD_STYLE, BUTTON_STYLE
from baligh.ui.ui_constants import LANGUAGE_MAP


def setup_layout(window):
    layout = QVBoxLayout()

    # ---------------- Translation Display ----------------
    window.translation_box = QTextEdit()
    window.translation_box.setReadOnly(True)
    window.translation_box.setStyleSheet(TRANSLATION_BOX_STYLE)

    # ---------------- Icons Path ----------------
    icon_path = os.path.join(os.path.dirname(__file__), "../icons")

    # ---------------- Copy Button ----------------
    window.copy_button = QPushButton()
    window.copy_button.setIcon(QIcon(os.path.join(icon_path, "copy-solid-full.svg")))
    window.copy_button.setFixedSize(24, 24)
    window.copy_button.setStyleSheet(BUTTON_STYLE)
    window.copy_button.clicked.connect(lambda: window.translation_box.selectAll() or window.translation_box.copy())

    # ---------------- Hide Button ----------------
    window.hide_button = QPushButton()
    window.hide_button.setIcon(QIcon(os.path.join(icon_path, "hide.svg")))
    window.hide_button.setFixedSize(24, 24)
    window.hide_button.setStyleSheet(BUTTON_STYLE)
    window.hide_button.clicked.connect(window.hide)

    # ---------------- Core Actions ----------------
    window.clipboard_toggle_action = QAction("Enable Clipboard Capture", window, checkable=True)
    window.clipboard_toggle_action.setChecked(True)
    window.clipboard_toggle_action.triggered.connect(lambda checked: setattr(window, "clipboard_enabled", checked))

    window.exit_action = QAction("Exit", window)
    window.exit_action.triggered.connect(window.close)

    # ---------------- Settings Button ----------------
    window.settings_button = QToolButton()
    window.settings_button.setIcon(QIcon(os.path.join(icon_path, "ellipsis.svg")))
    window.settings_button.setFixedSize(24, 24)
    window.settings_button.setPopupMode(QToolButton.InstantPopup)
    window.settings_button.setToolButtonStyle(Qt.ToolButtonIconOnly)
    window.settings_button.setStyleSheet(f"""
        QToolButton {{
            border-radius: 8px;
            background-color: rgba(255, 255, 255, 0.1);
        }}
        QToolButton:hover {{
            background-color: rgba(255, 255, 255, 0.25);
        }}
        QToolButton::menu-indicator {{
            image: none;
        }}
    """)

    # ---------------- Settings Menu ----------------
    window.settings_menu = QMenu(window)
    window.settings_menu.setWindowFlags(window.settings_menu.windowFlags() | Qt.FramelessWindowHint)
    window.settings_menu.setAttribute(Qt.WA_TranslucentBackground)
    window.settings_menu.setStyleSheet("""
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
    """)

    # Language nested menu
    language_menu = QMenu("Select Language", window.settings_menu)
    for language in LANGUAGE_MAP.keys():
        action = QAction(language, language_menu)
        action.triggered.connect(lambda checked, lang=language: window.on_language_selected(lang))
        language_menu.addAction(action)
    window.settings_menu.addMenu(language_menu)

    # Clipboard toggle & Exit
    window.settings_menu.addAction(window.clipboard_toggle_action)
    window.settings_menu.addSeparator()
    window.settings_menu.addAction(window.exit_action)

    window.settings_button.setMenu(window.settings_menu)

    # ---------------- Buttons Layout ----------------
    button_layout = QHBoxLayout()
    button_layout.addStretch()
    for btn in [window.copy_button, window.hide_button, window.settings_button]:
        button_layout.addWidget(btn)

    # ---------------- Card Layout ----------------
    card_layout = QVBoxLayout()
    card_layout.addLayout(button_layout)
    card_layout.addWidget(window.translation_box)

    card = QWidget()
    card.setLayout(card_layout)
    card.setStyleSheet(CARD_STYLE)
    card.setGraphicsEffect(None)

    layout.addWidget(card)
    window.setLayout(layout)
