#  AutoTokenizer => convert text to numbers (Tokens) and vice versa.
# (Sequence-to-Sequence Language Model) => load translation model
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class TranslationEngine:
    def __init__(self, model_path, device):
        # load model
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
        self.device = device

        self.model = self.model.to(device)
        self.model.eval()

    # method to translate.
    def translate(self, text, src_lang, tgt_lang, max_length=500, num_beams=1):
        # translate
        self.tokenizer.src_lang = src_lang
        inputs = self.tokenizer(text, return_tensors="pt")
        target_lang_id = self.tokenizer.convert_tokens_to_ids(tgt_lang)

        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.model.generate(
                input_ids=inputs['input_ids'],
                attention_mask=inputs['attention_mask'],
                max_length=max_length,
                forced_bos_token_id=target_lang_id,
                num_beams=num_beams,
                do_sample=False,
            )

            translated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return translated_text
