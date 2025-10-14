#  AutoTokenizer => convert text to numbers (Tokens) and vice versa.
# (Sequence-to-Sequence Language Model) => load translation model
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class TranslationEngine:
    """
    Core translation engine for Baligh Translator.

    This class loads and manages a sequence-to-sequence (Seq2Seq) language model
    (such as NLLB or MarianMT) and provides a clean API for text translation.

    Attributes:
        tokenizer (AutoTokenizer): Converts text to tokens and back.
        model (AutoModelForSeq2SeqLM): The loaded translation model.
        device (torch.device): The computation device ('cpu' or 'cuda').
    """
    def __init__(self, model_path: str, device: torch.device):
        """
        Initialize the translation engine by loading the model and tokenizer.

        Args:
            model_path (str): The path to the pretrained translation model.
            device (torch.device): The device to run the model on (CPU or GPU).

        Raises:
            OSError: If the model files cannot be found or loaded.
        """
        # load model
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
        self.device = device

        self.model = self.model.to(device)
        self.model.eval()

    # method to translate.
    def translate(self, text, src_lang, tgt_lang, max_length=500, num_beams=1) -> str:
        """
        Translate text from one language to another using the loaded model.

        Args:
            text (str): The input text to translate.
            src_lang (str): The source language code (e.g., "eng_Latn").
            tgt_lang (str): The target language code (e.g., "fra_Latn").
            max_length (int, optional): The maximum number of tokens to generate.
                Defaults to 500.
            num_beams (int, optional): The beam search width for translation quality.
                Higher values increase accuracy but slow down performance. Defaults to 1.

        Returns:
            str: The translated text.

        Example:
            >>> engine = TranslationEngine("path/to/model", torch.device("cpu"))
            >>> result = engine.translate("Hello world!", "eng_Latn", "arb_Arab")
            >>> print(result)
            "مرحبا بالعالم!"

        Notes:
            - Uses `forced_bos_token_id` to set the target language explicitly.
            - Runs inference under `torch.no_grad()` for better performance.
        """
        # Set source and target languages for the tokenizer
        self.tokenizer.src_lang = src_lang
        self.tokenizer.tgt_lang = tgt_lang

        # Encode input text
        inputs = self.tokenizer(text, return_tensors="pt")
        target_lang_id = self.tokenizer.convert_tokens_to_ids(tgt_lang)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        # Perform translation
        with torch.no_grad():
            outputs = self.model.generate(
                input_ids=inputs['input_ids'],
                attention_mask=inputs['attention_mask'],
                max_length=max_length,
                forced_bos_token_id=target_lang_id,
                num_beams=num_beams,
                do_sample=False,
            )

            # Decode translated text
            translated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return translated_text
