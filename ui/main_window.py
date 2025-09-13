import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QVBoxLayout, QMenuBar, QComboBox
from PyQt5.QtCore import Qt
import pyperclip
from PyQt5.QtCore import QTimer
from ..model.translation_engine import TranslationEngine
import json
import torch

base_dir = os.path.dirname(os.path.abspath(__file__)) 
config_path = os.path.join(base_dir, "../config.json")

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

        # config window
        self.setWindowTitle("بليــــغ")
        self.setWindowIcon(QIcon("icon.png"))

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)  # Always on Top
        self.setFixedSize(400, 200)  # fixed size

        # create menu
        menubar = QMenuBar(self)
        settings_menu = menubar.addMenu('Settings')

        # create main layout
        layout = QVBoxLayout()
        layout.setMenuBar(menubar)

        # change language option
        self.language_selector = QComboBox()
        self.language_selector.addItems(["Arabic", "French", "Spanish"])
        self.language_selector.currentIndexChanged.connect(self.language_changed)
        layout.addWidget(self.language_selector)

        # show translation
        self.translation_box = QTextEdit()
        self.translation_box.setReadOnly(True)
        self.translation_box.setText("Hello → مرحباً")  # for test
        layout.addWidget(self.translation_box)

        self.setLayout(layout)

        # clipboard monitor variables
        self.last_clipboard_text = ""
        self.last_check_time = 0

        # timer to monitor the clipboard
        self.timer = QTimer()
        self.timer.timeout.connect(self._check_clipboard)
        self.timer.start(300) # every 0.3 second

    # get copied text from clipboard
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

    # when user change target language
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TranslatorWindow()
    window.show()
    sys.exit(app.exec_())