import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import json
import time
import torch
from model.translation_engine import TranslationEngine

# load configuration
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# select device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# create engin (object)
engine = TranslationEngine(model_path=config["model_path"], device=device)

# translation test text
texts = [
    "Axis along which to sort. If None, the array is flattened before sorting. The default is -1, which sorts along the last axis."
]

# اختبار الترجمة مع حساب الزمن
for text in texts:
    start_time = time.time()
    translated = engine.translate(text, config["src_lang"], config["tgt_lang"], config["max_length"], config["num_beams"])
    end_time = time.time()
    print(f"\nOriginal: {text}")
    print(f"Translated: {translated}")
    print(f"Time: {end_time - start_time:.2f} sec")
