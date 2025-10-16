from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QTimer, Qt, QRect
from PyQt5.QtGui import QIcon
from baligh.ui.ui_window_setup import setup_window
from baligh.ui.ui_layout_setup import setup_layout
from baligh.ui.ui_tray_setup import setup_tray
from baligh.ui.ui_constants import LANGUAGE_MAP
from baligh.ui.window_animator import WindowAnimator


class TranslatorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self._drag_pos = None
        self.last_text = ""
        self.translation_service = None
        self.config = None
        self.current_language = None
        self.clipboard_enabled = True
        self._hovering = False
        self.setWindowIcon(QIcon("resources/icon.png"))

        # ---------------- Animator ----------------
        self.animator = WindowAnimator(self)

        # ---------------- Setup Window ----------------
        setup_window(self)
        setup_layout(self)
        setup_tray(self)
        self.language_map = LANGUAGE_MAP

        # ---------------- Position at top-right ----------------
        screen = QApplication.primaryScreen().availableGeometry()
        self.full_width = 400
        self.full_height = 300
        self.visible_width = 40  # الجزء الصغير عند الطي
        self.target_rect = QRect(
            screen.right() - self.full_width,
            20,
            self.full_width,
            self.full_height
        )
        self.setGeometry(self.target_rect)

    # ---------------- Show with animation ----------------
    def show_with_animation(self):
        self.show()
        self.animator.expand_right(self.full_width)

    # ---------------- Toggle visibility ----------------
    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.raise_()
            self.activateWindow()

    # ---------------- Move window ----------------
    def move_to(self, x, y):
        self.move(x, y)

    # ---------------- Mouse dragging ----------------
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_pos is not None and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
        event.accept()

    # ---------------- Hover events ----------------
    def enterEvent(self, event):
        self._hovering = True
        self.animator.expand_right(self.full_width)
        event.accept()

    def leaveEvent(self, event):
        self._hovering = False

        def collapse_if_needed():
            if not self._hovering and self.should_collapse():
                self.animator.collapse_right(self.visible_width)

        QTimer.singleShot(1000, collapse_if_needed)
        event.accept()

    # ---------------- Collapse logic ----------------
    def should_collapse(self):
        """Return True if window is close enough to left or right edge to allow collapse."""
        screen = self.screen()
        if not screen:
            screen = QApplication.primaryScreen()
        screen_geom = screen.availableGeometry()
        margin = 50  # tolerance in pixels
        x = self.geometry().x()
        return x >= screen_geom.right() - self.full_width - margin or x <= screen_geom.left() + margin

    # ---------------- Language selection / Clipboard ----------------
    def on_language_selected(self, lang: str):
        self.current_language = lang
        tgt_lang = self.language_map.get(lang)
        if tgt_lang and self.last_text:
            self.expand_if_collapsed()
            self.translate_text(self.last_text, tgt_lang)

    # ---------------- Clipboard / Expand logic ----------------
    def on_clipboard_text_copied(self, text: str):
        if not self.clipboard_enabled:
            return

        self.last_text = text
        tgt_lang = self.language_map.get(self.current_language, "arb_Arab")

        screen = self.screen() or QApplication.primaryScreen()
        screen_geom = screen.availableGeometry()

        # ✅ التمدد إذا كانت مطوية أو مخفية
        current_width = self.geometry().width()
        if current_width <= self.visible_width or self.isHidden():
            if self.isHidden():
                self.show()
                self.raise_()
                self.activateWindow()
            # أوقف أي حركة جارية ثم مدد النافذة
            if self.animator.animation.state() == self.animator.animation.Running:
                self.animator.animation.stop()
            self.animator.expand_right(self.full_width)

        # ترجمة النص
        self.translate_text(text, tgt_lang)

    def expand_if_collapsed(self):
        """Expand window if it is collapsed or hidden."""
        screen = self.screen() or QApplication.primaryScreen()
        screen_geom = screen.availableGeometry()

        current_width = self.geometry().width()
        if current_width <= self.visible_width or self.isHidden():
            if self.isHidden():
                self.show()
                self.raise_()
                self.activateWindow()
            # أوقف أي حركة جارية ثم مدد النافذة
            if self.animator.animation.state() == self.animator.animation.Running:
                self.animator.animation.stop()
            self.animator.expand_right(self.full_width)

    def translate_text(self, text: str, tgt_lang: str):
        if hasattr(self, "translation_box") and self.translation_box:
            self.translation_box.setText("Translating...")

        self.translation_service.translate_async(
            text=text,
            src_lang=self.config["src_lang"],
            tgt_lang=tgt_lang,
            max_length=self.config["max_length"],
            num_beams=self.config["num_beams"],
            callback=lambda translated: hasattr(self, "translation_box") and self.translation_box.setText(translated)
        )
        self.collapse_after_delay(10000)

    # ---------------- Collapse window after delay ----------------
    def collapse_after_delay(self, delay_ms=10000):
        QTimer.singleShot(delay_ms, lambda: self.check_auto_collapse())

    def check_auto_collapse(self):
        """Call this to auto-collapse if hovering is False and window is near edge."""
        if not self._hovering and self.should_collapse():
            self.animator.collapse_right(self.visible_width)
