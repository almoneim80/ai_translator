from PyQt5.QtCore import QThread, pyqtSignal
from .translation_engine import TranslationEngine


class TranslationThread(QThread):
    """
     Background worker thread for performing translation without blocking the UI.

     This thread runs the translation task using the provided TranslationEngine
     and emits the result asynchronously once the translation is complete.

     Signals
     -------
     finished : pyqtSignal(str)
         Emitted when the translation is finished, carrying the translated text.

     Parameters
     ----------
     engine : TranslationEngine
         The translation engine responsible for performing the translation.
     text : str
         The input text to be translated.
     src_lang : str
         The source language code (e.g., "en" for English).
     tgt_lang : str
         The target language code (e.g., "ar" for Arabic).
     max_length : int
         The maximum length of the translated output sequence.
     num_beams : int
         The number of beams for beam search (controls translation quality vs speed).
     """
    finished = pyqtSignal(str)

    def __init__(self, engine, text, src_lang, tgt_lang, max_length, num_beams):
        """
        Initialize the translation service.

        Parameters
        ----------
        engine : TranslationEngine
            The translation engine used to perform translations.
        """
        super().__init__()
        self.engine = engine
        self.text = text
        self.src_lang = src_lang
        self.tgt_lang = tgt_lang
        self.max_length = max_length
        self.num_beams = num_beams

    def run(self):
        """
        Executes the translation task in a separate thread.

        This method is automatically called when the thread starts.
        It performs translation using the engine and emits the
        resulting text via the `finished` signal.
        """
        result = self.engine.translate(
            self.text,
            self.src_lang,
            self.tgt_lang,
            self.max_length,
            self.num_beams
        )
        self.finished.emit(result)


class TranslationService:
    """
    High-level service that manages asynchronous translation tasks.

    This class provides an easy-to-use interface for running translations
    in background threads and updating the UI when translation is complete.

    Attributes
    ----------
    engine : TranslationEngine
        The translation engine instance used for all translation operations.
    thread : TranslationThread or None
        The currently running translation thread, if any.
    """
    def __init__(self, engine: TranslationEngine):
        self.engine = engine
        self.thread = None

    def translate_async(self, text, src_lang, tgt_lang, max_length, num_beams, callback):
        """
        Run a translation asynchronously in a separate thread.

        Parameters
        ----------
        text : str
            The input text to translate.
        src_lang : str
            The source language code.
        tgt_lang : str
            The target language code.
        max_length : int
            The maximum output length for the translation.
        num_beams : int
            Number of beams for beam search.
        callback : callable
            Function to call when translation finishes. Receives one argument — the translated text.

        Notes
        -----
        - This method starts a new background thread for translation.
        - Once the translation completes, the provided callback is invoked automatically.
        """
        self.thread = TranslationThread(self.engine, text, src_lang, tgt_lang, max_length, num_beams)
        self.thread.finished.connect(callback)
        self.thread.start()
