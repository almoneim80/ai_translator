from PyQt5.QtCore import QPropertyAnimation, QRect, QEasingCurve

class WindowAnimator:
    """
    Handles smooth expand/collapse animations for the translator window.
    """

    def __init__(self, window):
        self.window = window
        self.animation = QPropertyAnimation(window, b"geometry")
        self.animation.setDuration(400)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)

    def collapse_right(self, visible_width: int = 40):
        """Collapse window to the right, leaving a small visible strip."""
        self.animation.stop()
        geom = self.window.geometry()
        screen = self.window.screen().availableGeometry()
        end_rect = QRect(
            screen.right() - visible_width,
            geom.y(),
            visible_width,
            geom.height()
        )
        self.animation.setStartValue(geom)
        self.animation.setEndValue(end_rect)
        self.animation.start()

    def expand_right(self, full_width: int = 400):
        """Expand window to full width from collapsed state."""
        self.animation.stop()
        geom = self.window.geometry()
        screen = self.window.screen().availableGeometry()
        target_rect = QRect(
            screen.right() - full_width,
            geom.y(),
            full_width,
            geom.height()
        )
        self.animation.setStartValue(geom)
        self.animation.setEndValue(target_rect)
        self.animation.start()
