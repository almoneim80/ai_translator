import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget,QTextEdit, QVBoxLayout, QMenuBar, QComboBox, QSystemTrayIcon, QMenu, QAction, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
import keyboard
import pyperclip
from PyQt5.QtCore import QTimer
from ..model.translation_engine import TranslationEngine
import json
import torch

base_dir = os.path.dirname(os.path.abspath(__file__)) 
config_path = os.path.join(base_dir, "../config.json")
icon_path = os.path.join(base_dir, "../resources/icon.png")

class TranslatorWindow(QWidget):
    def __init__(self):
        super().__init__()

        with open(config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.engine = TranslationEngine(model_path=self.config["model_path"], device=device)

        # Map between the language name in the list and the language code in the model
        self.language_map = {
            "Arabic": "arb_Arab",
            "French": "fra_Latn",
            "Spanish": "spa_Latn"
        }

        # ---------------------- config window ---------------------------------
        self.setWindowTitle("بليــــغ")
        self.setWindowIcon(QIcon(icon_path))
        #self.setWindowOpacity(0.9)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)  # Always on Top
        self.setFixedSize(400, 200)  # fixed size
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.85);
            color: #333333;
            font-family: 'Segoe UI', Tahoma, sans-serif;
            font-size: 14px;
            border-radius: 15px;
        """)
        self.setStyleSheet("""
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #e0f7fa, stop:1 #ffffff
            );
            border-radius: 15px;
        """)

        # create main layout
        layout = QVBoxLayout()

        # change language option
        self.language_selector = QComboBox()
        self.language_selector.addItems(["Arabic", "French", "Spanish"])
        self.language_selector.currentIndexChanged.connect(self.language_changed)
        self.language_selector.setStyleSheet("""
        background-color: #ffffff;
        border-radius: 8px;
        border: 1px solid #cccccc;
        padding: 4px;
    """)
        layout.addWidget(self.language_selector)

        # show translation
        self.translation_box = QTextEdit()
        self.translation_box.setReadOnly(True)
        self.translation_box.setText("Hello → مرحباً")  # for test
        self.translation_box.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.9);
            border-radius: 10px;
            border: 1px solid #cccccc;
            padding: 10px;
            font-size: 14px;
            color: #222222;
        """)
        layout.addWidget(self.translation_box)

        # Shadow / Drop shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(Qt.gray)
        self.setGraphicsEffect(shadow)

        self.setLayout(layout)

        # clipboard monitor variables
        self.last_clipboard_text = ""
        self.last_check_time = 0

        # timer to monitor the clipboard
        self.timer = QTimer()
        self.timer.timeout.connect(self._check_clipboard)
        self.timer.start(300) # every 0.3 second


        # System Tray
        self.tray_icon = QSystemTrayIcon(QIcon(icon_path), self)
        self.tray_menu = QMenu()

        show_action = QAction("Show Window", self.tray_menu)
        show_action.triggered.connect(self.show)
        self.tray_menu.addAction(show_action)

        hide_action = QAction("Hide Window", self.tray_menu)
        hide_action.triggered.connect(self.hide)
        self.tray_menu.addAction(hide_action)

        exit_action = QAction("Exit", self.tray_menu)
        exit_action.triggered.connect(QApplication.instance().quit)
        self.tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

        # keyboard shortcut to show/hide window
        keyboard.add_hotkey("ctrl+shift+alt", self.toggle_visibility)

    # ----------------------------- show tray icon menu ------------------------------
    def on_tray_icon_activated(self, reason):
        print("Tray activated reason:", reason)
        if reason == QSystemTrayIcon.Trigger: # Left clicks
            if self.isVisible():
                self.hide()
            else:
                self.show()
                self.raise_() # window on top
                self.activateWindow()

    # ----------------------------- get copied text from clipboard ------------------------------
    def _check_clipboard(self):
        copy_text = pyperclip.paste().strip()
        if copy_text and copy_text != self.last_clipboard_text:
            if len(copy_text) < 3:
                self.translation_box.setText("❗ Text too short to translate.")
                return
            
            self.last_clipboard_text = copy_text

            tgt_lang = None
            selected_language = self.language_selector.currentText()
            if selected_language == "Arabic":
                tgt_lang = "arb_Arab"
            elif selected_language == "French":
                tgt_lang = "fra_Latn"
            elif selected_language == "Spanish":
                tgt_lang = "spa_Latn"


            traslated = self.engine.translate(
                copy_text,
                self.config["src_lang"],
                tgt_lang,
                self.config["max_length"],
                self.config["num_beams"]
            )
            self.translation_box.setText(traslated)

    # ------------------------------ change target language -----------------------------------
    def language_changed(self):
        selected_language = self.language_selector.currentText()
        lang_code = self.language_map[selected_language]

        current_text = self.last_clipboard_text
        if current_text:
            translated = self.engine.translate(
                current_text,
                self.config["src_lang"],
                lang_code,
                self.config["max_length"],
                self.config["num_beams"]
            )
            self.translation_box.setText(translated)
        print(f"Target language changed to: {selected_language} ({lang_code})")

    # ----------------------------- toggle to show window using shortcut ------------------------------
    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.raise_()
            self.activateWindow()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TranslatorWindow()
    window.show()
    sys.exit(app.exec_())