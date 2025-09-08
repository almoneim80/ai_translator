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


class TranslatorWindow(QWidget):
    def __init__(self):
        super().__init__()

        with open("config.json", "r", encoding="utf-8") as f:
            self.config = json.load(f)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.engin = TranslationEngine(model_path=self.config["model_path"], device=device)


        # config window
        self.setWindowTitle("Baligh Translator")
        self.setWindowIcon(QIcon("icon.png"))

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)  # Always on Top
        self.setFixedSize(400, 400)  # fixed size

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
            self.last_clipboard_text = copy_text
            traslated = self.engine.translate(
                copy_text,
                self.config["src_lang"],
                self.config["tgt_lang"],
                self.config["max_length"],
                self.config["num_beams"]
            )
            self.translation_box.setText(traslated)

    def language_changed(self):
        selected_language = self.language_selector.currentText()
        print(f"Selected target language: {selected_language}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TranslatorWindow()
    window.show()
    sys.exit(app.exec_())