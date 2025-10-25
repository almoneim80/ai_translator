from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import QTimer, Qt, QRect
from PyQt5.QtGui import QIcon
from baligh.ui.ui_window_setup import setup_window
from baligh.ui.ui_layout_setup import setup_layout
from baligh.ui.ui_tray_setup import setup_tray
from baligh.ui.ui_constants import (LANGUAGE_MAP, WINDOW_ICON_PATH, TRANSLATOR_WINDOW_FULL_WIDTH,
                                    TRANSLATOR_WINDOW_FULL_HEIGHT, TRANSLATOR_WINDOW_VISIBLE_WIDTH, WINDOW_TOP_MARGIN,
                                    WINDOW_COLLAPSE_DELAY_MS, TRANSLATION_COLLAPSE_DELAY_MS, WINDOW_EDGE_MARGIN,
                                    LAST_TRANSLATED_TEXT, HOVER_DEFAULT, CLIPBOARD_ENABLED_DEFAULT, RIGHT_MARGIN)
from baligh.ui.window_animator import WindowAnimator
from baligh.services.localization_service import get_text


class TranslatorWindow(QWidget):
    """
    The main floating translator window.

    This window handles:
      - UI setup and layout.
      - Animated show/hide behavior.
      - Text translation workflow.
      - Clipboard monitoring and automatic translation.
      - Mouse-based window dragging and hover collapse logic.
    """
    def __init__(self):
        super().__init__()
        self._drag_pos = None
        self.last_text = LAST_TRANSLATED_TEXT
        self.translation_service = None
        self.config = None
        self.current_language = None
        self.clipboard_enabled = CLIPBOARD_ENABLED_DEFAULT
        self._hovering = HOVER_DEFAULT
        self.setWindowIcon(QIcon(WINDOW_ICON_PATH))

        # ---------------- Animator ----------------
        self.animator = WindowAnimator(self)

        # ---------------- Setup Window ----------------
        setup_window(self)
        setup_layout(self)
        setup_tray(self)
        self.language_map = LANGUAGE_MAP

        # ---------------- Position at top-right ----------------
        screen = QApplication.primaryScreen().availableGeometry()
        self.full_width = TRANSLATOR_WINDOW_FULL_WIDTH
        self.full_height = TRANSLATOR_WINDOW_FULL_HEIGHT
        self.visible_width = TRANSLATOR_WINDOW_VISIBLE_WIDTH
        self.target_rect = QRect(
            screen.right() - self.full_width - RIGHT_MARGIN,
            WINDOW_TOP_MARGIN,
            self.full_width,
            self.full_height
        )
        self.setGeometry(self.target_rect)

    # ---------------- Show with animation ----------------
    def show_with_animation(self):
        """
        Show the translator window with an expand animation.

        For beginners:
            Makes the window appear smoothly by expanding to its full width.
        Technical:
            Calls `self.animator.expand_right()` to play the right-side expansion animation
            after showing the widget.
        """
        self.show()
        self.animator.expand_right(self.full_width)

    # ---------------- Toggle visibility ----------------
    def toggle_visibility(self):
        """
        Toggle the window’s visibility (show or hide).

        For beginners:
            If the window is hidden, show it. If it’s visible, hide it.
        Technical:
            Ensures the window is raised and activated if shown, allowing it to receive focus.
        """
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.raise_()
            self.activateWindow()

    # ---------------- Move window ----------------
    def move_to(self, x, y):
        """
        Move the window to a specific (x, y) position on the screen.

        For beginners:
            Relocates the window visually.
        Technical:
            A thin wrapper around QWidget.move() for programmatic positioning.
        """
        self.move(x, y)

    # ---------------- Mouse dragging ----------------
    def mousePressEvent(self, event):
        """
        Record the position where the user started dragging the window.

        For beginners:
            Allows the window to be dragged around using the mouse.
        Technical:
            Stores the difference between the global cursor position and the window's top-left corner.
        """
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """
        Move the window while the user drags it.

        For beginners:
            Lets the user move the window by clicking and dragging.
        Technical:
            Continuously repositions the window while the left mouse button is pressed.
        """
        if self._drag_pos is not None and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        """
        Stop window dragging when the mouse button is released.

        For beginners:
            Ends the drag operation.
        Technical:
            Clears `_drag_pos` so the window no longer follows the cursor.
        """
        self._drag_pos = None
        event.accept()

    # ---------------- Hover events ----------------
    def enterEvent(self, event):
        """
        Triggered when the mouse cursor enters the window area.

        For beginners:
            Expands the window fully when hovered.
        Technical:
            Sets `_hovering` to True and plays the right-side expand animation.
        """
        self._hovering = True
        self.animator.expand_right(self.full_width)
        event.accept()

    def leaveEvent(self, event):
        """
        Triggered when the mouse cursor leaves the window area.

        For beginners:
            Automatically collapses the window after a short delay if not interacting.
        Technical:
            Checks `_menu_open` flag to prevent collapsing while menus are active.
            Uses QTimer to defer collapse.
        """
        self._hovering = False

        def collapse_if_needed():
            if not self._hovering and not getattr(self, "_menu_open", False) and self.should_collapse():
                self.animator.collapse_right(self.visible_width)

        QTimer.singleShot(WINDOW_COLLAPSE_DELAY_MS, collapse_if_needed)
        event.accept()

    # ---------------- Collapse logic ----------------
    def should_collapse(self):
        """
        Determine if the window is near an edge and eligible for collapse.

        For beginners:
            Checks if the window is close enough to the screen’s edge to fold automatically.
        Technical:
            Compares current X position with screen geometry using `WINDOW_EDGE_MARGIN` tolerance.
        Returns:
            bool: True if window can auto-collapse, otherwise False.
        """
        screen = self.screen()
        if not screen:
            screen = QApplication.primaryScreen(self)
        screen_geom = screen.availableGeometry()
        margin = WINDOW_EDGE_MARGIN  # tolerance in pixels
        x = self.geometry().x()
        return x >= screen_geom.right() - self.full_width - margin or x <= screen_geom.left() + margin

    # ---------------- Language selection / Clipboard ----------------
    def on_language_selected(self, lang: str):
        """
        Called when the user selects a target language.

        For beginners:
            Updates the translation language and re-translates the last copied text.
        Technical:
            Uses `LANGUAGE_MAP` to resolve language codes and triggers translation if `last_text` exists.
        """
        self.current_language = lang
        tgt_lang = self.language_map.get(lang)
        if tgt_lang and self.last_text:
            self.expand_if_collapsed()
            self.translate_text(self.last_text, tgt_lang)

    # ---------------- Clipboard / Expand logic ----------------
    def on_clipboard_text_copied(self, text: str):
        """
        Handle new clipboard text (auto-translate feature).

        For beginners:
            Automatically translates any new text copied to the clipboard.
        Technical:
            - Checks if clipboard translation is enabled.
            - Expands window and triggers translation.
            - Stops any running animation before starting a new one.
        """
        if not self.clipboard_enabled:
            return

        self.last_text = text
        tgt_lang = self.language_map.get(self.current_language, "arb_Arab")

        # Ensure that the window is always visible and maximized
        if self.isHidden():
            self.show()
            self.raise_()
            self.activateWindow()

        if self.animator.animation.state() == self.animator.animation.Running:
            self.animator.animation.stop()

        self.animator.expand_right(self.full_width)

        # Translation of the text
        self.translate_text(text, tgt_lang)

    def expand_if_collapsed(self):
        """
        Expand the window if it’s currently collapsed or hidden.

        For beginners:
            Makes sure the window is visible and fully open before showing translation.
        Technical:
            - Stops ongoing animations.
            - Uses `expand_right()` to ensure full visibility.
        """
        screen = self.screen() or QApplication.primaryScreen(self)
        screen_geom = screen.availableGeometry()

        current_width = self.geometry().width()
        if current_width <= self.visible_width or self.isHidden():
            if self.isHidden():
                self.show()
                self.raise_()
                self.activateWindow()
            # Stop any ongoing movement and then extend the window.
            if self.animator.animation.state() == self.animator.animation.Running:
                self.animator.animation.stop()
            self.animator.expand_right(self.full_width)

    def translate_text(self, text: str, tgt_lang: str):
        """
        Perform asynchronous translation of the given text.

        For beginners:
            Translates the given text and shows the result in the translation box.
        Technical:
            - Uses `translation_service.translate_async()` for non-blocking translation.
            - Displays a placeholder text before translation finishes.
            - Triggers delayed collapse after completion.
        """
        if hasattr(self, "translation_box") and self.translation_box:
            self.translation_box.setText(get_text("Default_Translation_Card"))

        self.translation_service.translate_async(
            text=text,
            src_lang=self.config["src_lang"],
            tgt_lang=tgt_lang,
            max_length=self.config["max_length"],
            num_beams=self.config["num_beams"],
            callback=lambda translated: hasattr(self, "translation_box") and self.translation_box.setText(translated)
        )
        self.collapse_after_delay(TRANSLATION_COLLAPSE_DELAY_MS)

    # ---------------- Collapse window after delay ----------------
    def collapse_after_delay(self, delay_ms=TRANSLATION_COLLAPSE_DELAY_MS):
        """
        Schedule automatic window collapse after translation delay.

        For beginners:
            Waits a short time before folding the window automatically.
        Technical:
            Uses QTimer to call `check_auto_collapse()` after `delay_ms`.
        """
        QTimer.singleShot(delay_ms, lambda: self.check_auto_collapse())

    def check_auto_collapse(self):
        """
        Perform the final check before auto-collapsing the window.

        For beginners:
            Collapses the window if not hovered and no menu is open.
        Technical:
            Prevents collapsing when `_menu_open` is True or `_hovering` is True.
            Ensures the window is near the edge before triggering collapse animation.
        """
        if not getattr(self, "_menu_open", False) and not self._hovering and self.should_collapse():
            self.animator.collapse_right(self.visible_width)
