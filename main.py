import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import sys
import torch
from PyQt5.QtWidgets import QApplication
from baligh.ui.main_window import TranslatorWindow
from baligh.model.translation_engine import TranslationEngine
from baligh.model.translation_service import TranslationService
from baligh.services.config_loader import load_config
from baligh.services.clipboard_service import ClipboardService
from baligh.services.keyboard_service import KeyboardService
import ctypes

def main():
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u"ai_translator.app")
    app = QApplication(sys.argv)

    # ------------------- Load Configuration -------------------
    config = load_config()

    # ------------------- Initialize Translation Engine -------------------
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    engine = TranslationEngine(model_path=config["model_path"], device=device)
    translation_service = TranslationService(engine)

    # ------------------- Initialize UI -------------------
    window = TranslatorWindow()
    window.translation_service = translation_service
    window.config = config
    window.show()
    window.isLeftToRight()

    # ------------------- Clipboard Handling -------------------
    def on_clipboard_text_copied(text: str):
        if not getattr(window, "clipboard_enabled", True):
            return
        window.on_clipboard_text_copied(text)

    window.clipboard_service = ClipboardService(callback=on_clipboard_text_copied)

    # Link Toggle to enable/disable monitoring
    window.clipboard_toggle_action.triggered.connect(
        lambda checked: window.clipboard_service.start() if checked else window.clipboard_service.stop())

    # ------------------- Keyboard Shortcut -------------------
    KeyboardService(toggle_callback=window.toggle_visibility)

    # ------------------- Start Application -------------------
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
