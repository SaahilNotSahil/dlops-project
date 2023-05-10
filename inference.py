import io
import json
import time
import urllib.request

import numpy as np
import requests
import torch
from PIL import Image

from ViLT.vilt.datamodules.datamodule_base import get_pretrained_tokenizer
from ViLT.vilt.transforms import pixelbert_transform

device = torch.device("cpu")


def _setup():
    _config = json.load(open("/workspace/config.json", "r"))

    tokenizer = get_pretrained_tokenizer(_config["tokenizer"])

    with urllib.request.urlopen(
        "https://github.com/dandelin/ViLT/releases/download/200k/vqa_dict.json"
    ) as url:
        id2ans = json.loads(url.read().decode())

    model = torch.load("/workspace/vilt_vqa2.ckpt")
    model.setup("test")
    model.to(device)
    model.eval()

    return model, tokenizer, id2ans


def infer(model, tokenizer, id2ans, question, image=None, url=None):
    try:
        if image:
            image = Image.open(io.BytesIO(image)).convert("RGB")
        elif url:
            res = requests.get(url)
            image = Image.open(io.BytesIO(res.content)).convert("RGB")

        img = pixelbert_transform(size=384)(image)
        img = img.unsqueeze(0).to(device)
    except Exception as e:
        return e

    batch = {"text": [question], "image": [img]}

    with torch.no_grad():
        encoded = tokenizer(batch["text"])
        batch["text_ids"] = torch.tensor(encoded["input_ids"]).to(device)
        batch["text_labels"] = torch.tensor(
            encoded["input_ids"]).to(device)
        batch["text_masks"] = torch.tensor(
            encoded["attention_mask"]).to(device)

        start = time.time()

        infer = model.infer(batch)
        vqa_logits = model.vqa_classifier(infer["cls_feats"])

        end = time.time()

        print(f"Inference Time: {end - start:.3f}s")

    answer = id2ans[str(vqa_logits.argmax().item())]

    return [np.array(image), answer]
