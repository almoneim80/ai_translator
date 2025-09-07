"""
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextEdit, QVBoxLayout, QMenuBar, QComboBox
from PyQt5.QtCore import Qt


class TranslatorWindow(QWidget):
    def __init__(self):
        super().__init__()

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

    def language_changed(self):
        selected_language = self.language_selector.currentText()
        print(f"Selected target language: {selected_language}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TranslatorWindow()
    window.show()
    sys.exit(app.exec_())
"""