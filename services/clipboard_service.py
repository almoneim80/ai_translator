from PyQt5.QtCore import QTimer
import pyperclip


class ClipboardService:
    """
    Monitors the system clipboard and triggers a callback when new text is copied.

    This service periodically checks the clipboard for changes using a QTimer.
    When it detects a new text value, it calls the provided callback function,
    allowing integration with translation or text-processing pipelines.

    Attributes:
        callback (Callable[[str], None]): Function to call when new text is detected.
        last_clipboard_text (str): Stores the most recently processed clipboard text.
        timer (QTimer): Periodic timer to check clipboard content.
    """

    def __init__(self, callback, interval: int = 300):
        """
        Initialize the clipboard monitoring service.

        Args:
            callback (Callable[[str], None]): Function to call when new clipboard text is detected.
                The function should accept a single string argument representing the copied text.
            interval (int, optional): The polling interval in milliseconds. Defaults to 300.

        Example:
            >>> def handle_text(text):
            ...     print(f"New clipboard text: {text}")
            >>> service = ClipboardService(callback=handle_text, interval=500)
        """
        self.callback = callback
        self.last_clipboard_text = ""
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_clipboard)
        self.interval = interval
        self.running = False
        self.start()

    def start(self):
        if not self.running:
            self.timer.start(self.interval)
            self.running = True

    def stop(self):
        if self.running:
            self.timer.stop()
            self.running = False

    def check_clipboard(self):
        """
        Check the system clipboard for new text.

        If the clipboard contains text that differs from the last processed
        text and is longer than two characters, the callback function is triggered.
        """
        text = pyperclip.paste().strip()
        if text and text != self.last_clipboard_text and len(text) > 2:
            self.last_clipboard_text = text
            self.callback(text)
