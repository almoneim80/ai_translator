import keyboard


class KeyboardService:
    """
    A service for managing global keyboard shortcuts.

    This class listens for a specific key combination and triggers
    a callback function when pressed. Useful for toggling visibility
    of an application window or performing other global actions.
    """
    def __init__(self, toggle_callback):
        """
        Initialize the KeyboardService with a callback function.

        Args:
            toggle_callback (Callable): A function to be executed when
                the hotkey (Ctrl + Shift + Alt) is pressed. Typically used
                to show or hide a window.

        Notes:
            - The hotkey combination is registered globally using the
              `keyboard` library.
            - Requires administrative privileges on some systems
              (especially Windows) to capture global hotkeys.
        """
        keyboard.add_hotkey("ctrl+shift+alt", toggle_callback)
