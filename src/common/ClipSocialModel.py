from PIL import Image
from transformers import CLIPProcessor, CLIPModel

from src.common.CLIPResultObject import CLIPResultObject
from src.common.data_handler import process_images_k_by_k

_use_unix = True

class CLIPSocialModel:
    def __init__(self, model_path):
        self._processor = CLIPProcessor.from_pretrained(model_path)
        self._model = CLIPModel.from_pretrained(model_path)
        self.results : dict[str, CLIPResultObject] = {}

    @staticmethod
    def split_text_with_overlap(text, n = 10, k = 3):
        words = text.split()
        parts = []
        for i in range(0, len(words), n - k):
            part = words[i : i + n]
            part.append(" ".join(part))
            if i + n >= len(words):
                break
        return parts

    def assign_probs_caption(self, image_path : str, captions : list[str]):
        image = Image.open(image_path)
        inputs = self._processor(text=captions, images=image, return_tensors="pt", padding=True)
        outputs = self._model(**inputs)
        logits_per_image = outputs.logits_per_image
        probs = logits_per_image.softmax(dim=1)
        caption_probs = {}
        for i, caption in enumerate(captions):
            caption_probs[caption] = probs[i]
        result = CLIPResultObject(image_path, caption_probs)
        self.results[image_path] = result

    def process_using_db(self, database_path):
        for image_path, surrounding_text in process_images_k_by_k(database_path):
            if _use_unix:
                image_path = image_path.replace("\\", r"/")
            if len(surrounding_text) == 0:
                pass
            else:
                captions = self.split_text_with_overlap(surrounding_text)
                self.assign_probs_caption(image_path, captions)