import os
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from baligh.ui.ui_window_setup import setup_window
from baligh.ui.ui_layout_setup import setup_layout
from baligh.ui.ui_tray_setup import setup_tray
from baligh.ui.ui_constants import LANGUAGE_MAP
from PyQt5.QtGui import QIcon


class TranslatorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self._drag_pos = None
        self.last_text = ""
        self.translation_service = None
        self.config = None
        self.current_language = None
        self.setWindowIcon(QIcon("resources/icon.png"))

        # Preparing the window
        setup_window(self)
        # Preparing the interface layout
        setup_layout(self)
        # Setting up the system menu (Tray)
        setup_tray(self)

        # Definition of language map for access to services
        self.language_map = LANGUAGE_MAP

        # ---------------- Position at top-right ----------------
        screen = self.screen().availableGeometry()
        x = screen.right() - self.width() + 10
        y = screen.top() + 20
        self.move(x, y)

    # ---------------- Shortcut / Toggle Visibility ----------------
    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.raise_()
            self.activateWindow()

    # ---------------- Control where the translator window appears ----------------
    def move_to(self, x, y):
        """
        Move the window to a specific position on the screen.

        Args:
            x (int): X-coordinate (pixels)
            y (int): Y-coordinate (pixels)
        """
        self.move(x, y)

    # ---------------- Mouse dragging ----------------
    def mousePressEvent(self, event):
        """
        Handle mouse press event to initiate window dragging.

        Captures the offset between the mouse click position and the
        top-left corner of the window. Only triggers for left mouse button clicks.

        Args:
            event (QMouseEvent): The mouse press event containing position and button info.
        """
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """
        Handle mouse move event to drag the window.

        Moves the window following the mouse while maintaining the initial offset
        captured during mouse press. Only active while left mouse button is held.

        Args:
            event (QMouseEvent): The mouse move event containing current position.
        """
        if self._drag_pos is not None and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        """
        Handle mouse release event to stop window dragging.

        Resets the drag state so the window stops following the mouse.

        Args:
            event (QMouseEvent): The mouse release event.
        """
        self._drag_pos = None
        event.accept()

    # ---------------- Language selection from tray ----------------
    def on_language_selected(self, lang: str):
        """
        Handle language selection from the tray menu.

        Args:
            lang (str): The selected target language.
        """
        self.current_language = lang
        tgt_lang = self.language_map.get(lang)
        if tgt_lang and hasattr(self, "last_text") and self.last_text:
            self.translation_box.setText("Translating...")
            self.translation_service.translate_async(
                text=self.last_text,
                src_lang=self.config["src_lang"],
                tgt_lang=tgt_lang,
                max_length=self.config["max_length"],
                num_beams=self.config["num_beams"],
                callback=lambda translated: self.translation_box.setText(translated)
            )

