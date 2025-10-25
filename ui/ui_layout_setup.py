from PyQt5.QtWidgets import (
    QVBoxLayout, QTextEdit, QWidget, QPushButton, QHBoxLayout,
    QAction, QMenu, QToolButton
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import os
from baligh.ui.ui_styles import (TRANSLATION_BOX_STYLE, CARD_STYLE, BUTTON_STYLE, SETTINGS_MENU_STYLE,
                                 SETTINGS_BUTTON_STYLE)
from baligh.ui.ui_constants import (LANGUAGE_MAP, COPY_ICON_PATH, HIDE_ICON_PATH, More_ICON_PATH, SETTINGS_ICON_HEIGH,
                                    SETTINGS_ICON_WIDTH)
from baligh.services.localization_service import get_text


def setup_layout(window):
    layout = QVBoxLayout()

    # ---------------- Translation Display ----------------
    window.translation_box = QTextEdit()
    window.translation_box.setReadOnly(True)
    window.translation_box.setStyleSheet(TRANSLATION_BOX_STYLE)

    # ---------------- Copy Button ----------------
    window.copy_button = QPushButton()
    window.copy_button.setIcon(QIcon(os.path.join(COPY_ICON_PATH)))
    window.copy_button.setFixedSize(SETTINGS_ICON_WIDTH, SETTINGS_ICON_HEIGH)
    window.copy_button.setStyleSheet(BUTTON_STYLE)
    window.copy_button.clicked.connect(lambda: window.translation_box.selectAll() or window.translation_box.copy())

    # ---------------- Hide Button ----------------
    window.hide_button = QPushButton()
    window.hide_button.setIcon(QIcon(os.path.join(HIDE_ICON_PATH)))
    window.hide_button.setFixedSize(SETTINGS_ICON_WIDTH, SETTINGS_ICON_HEIGH)
    window.hide_button.setStyleSheet(BUTTON_STYLE)
    window.hide_button.clicked.connect(window.hide)

    # ---------------- Core Actions ----------------
    window.clipboard_toggle_action = QAction(get_text("Enable_Clipboard_Capture_Setting"), window, checkable=True)
    window.clipboard_toggle_action.setChecked(True)
    window.clipboard_toggle_action.triggered.connect(lambda checked: setattr(window, "clipboard_enabled", checked))

    window.exit_action = QAction(get_text("Exit_Setting"), window)
    window.exit_action.triggered.connect(window.close)

    # ---------------- Settings Button ----------------
    window.settings_button = QToolButton()
    window.settings_button.setIcon(QIcon(os.path.join(More_ICON_PATH)))
    window.settings_button.setFixedSize(SETTINGS_ICON_WIDTH, SETTINGS_ICON_HEIGH)
    window.settings_button.setPopupMode(QToolButton.InstantPopup)
    window.settings_button.setToolButtonStyle(Qt.ToolButtonIconOnly)
    window.settings_button.setStyleSheet(SETTINGS_BUTTON_STYLE)

    # ---------------- Settings Menu ----------------
    window.settings_menu = QMenu(window)
    # احتفظنا بالستايل لكنه لم يعد يغيّر سلوك الطي — سنمنع الطي عبر العلم _menu_open
    window.settings_menu.setStyleSheet(SETTINGS_MENU_STYLE)

    # ---------------- NEW: علم منع الطي أثناء عرض القائمة ----------------
    # نعرّف العلم ونربطه بإشارات القائمة حتى نعرف متى تكون مفتوحة
    window._menu_open = False
    # aboutToShow / aboutToHide موجودان في QMenu — نربطهما لتغيير العلم تلقائياً
    try:
        window.settings_menu.aboutToShow.connect(lambda: setattr(window, "_menu_open", True))
        window.settings_menu.aboutToHide.connect(lambda: setattr(window, "_menu_open", False))
    except Exception as e:
        # In the event of any unusual circumstances, the flag will be present and will be controlled manually if necessary.
        print(f"Warning: Could not connect signals: {e}")
    # --------------------------------------------------------------

    # Language nested menu
    language_menu = QMenu(get_text("Select_Language_Setting"), window.settings_menu)
    for language in LANGUAGE_MAP.keys():
        action = QAction(language, language_menu)
        action.triggered.connect(lambda checked, lang=language: window.on_language_selected(lang))
        language_menu.addAction(action)
    window.settings_menu.addMenu(language_menu)

    # Clipboard toggle & Exit
    window.settings_menu.addAction(window.clipboard_toggle_action)
    window.settings_menu.addSeparator()
    window.settings_menu.addAction(window.exit_action)

    # ---------------- Safety: تحميل القائمة بطريقة قياسية على الزر ----------------
    # نستخدم setMenu + InstantPopup كما كان — لكن العلم _menu_open يمنع الطي أثناء ظهور القائمة.
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
