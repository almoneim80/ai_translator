from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from baligh.ui.ui_constants import TRAY_ICON_PATH
from baligh.ui.ui_constants import LANGUAGE_MAP
from baligh.services.localization_service import get_text


def setup_tray(window):
    """
    Configure the system tray icon and its menu for the main window.

    Args:
        window (QWidget): The main application window.
    """
    window.tray_icon = QSystemTrayIcon(QIcon(TRAY_ICON_PATH), window)
    tray_menu = QMenu()

    # ---------------- Language Selection Submenu ----------------
    language_menu = QMenu(get_text("Select_Language_Setting"), tray_menu)
    for language in LANGUAGE_MAP.keys():
        action = QAction(language, language_menu)
        action.triggered.connect(lambda checked, lang=language: window.on_language_selected(lang))
        language_menu.addAction(action)
    tray_menu.addMenu(language_menu)

    # ---------------- Toggle Clipboard ----------------
    window.clipboard_toggle_action = QAction(get_text("Enable_Clipboard_Capture_Setting"), tray_menu, checkable=True)
    window.clipboard_toggle_action.setChecked(True)
    window.clipboard_toggle_action.triggered.connect(lambda checked: setattr(window, "clipboard_enabled", checked))
    tray_menu.addAction(window.clipboard_toggle_action)

    # ---------------- Show / Hide / Exit ----------------
    show_action = QAction(get_text("Show_Window_Setting"), tray_menu)
    show_action.triggered.connect(window.show)
    tray_menu.addAction(show_action)

    hide_action = QAction(get_text("Hide_Window_Setting"), tray_menu)
    hide_action.triggered.connect(window.hide)
    tray_menu.addAction(hide_action)

    exit_action = QAction(get_text("Exit_Setting"), tray_menu)
    exit_action.triggered.connect(window.close)
    tray_menu.addAction(exit_action)

    window.tray_icon.setContextMenu(tray_menu)
    window.tray_icon.show()
