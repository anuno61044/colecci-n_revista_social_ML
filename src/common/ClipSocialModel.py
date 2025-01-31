import os.path

from PIL import Image
from transformers import CLIPProcessor, CLIPModel

from src.common.CLIPResultObject import CLIPResultObject
from src.common.data_handler import process_images_k_by_k, get_image_captions
from src.common.social_model import SocialModel

class CLIPSocialModel(SocialModel):
    def __init__(self, model_path):
        self._processor = CLIPProcessor.from_pretrained(model_path)
        self._model = CLIPModel.from_pretrained(model_path)

    @staticmethod
    def split_text_with_overlap(text, n = 10, k = 3):
        words = text.split()
        parts = []
        for i in range(0, len(words), n - k):
            part = words[i : i + n]
            parts.append(" ".join(part))
            if i + n >= len(words):
                break
        return parts

    def assign_probs_caption(self, image : Image, captions : list[str]):
        inputs = self._processor(text=captions, images=image, return_tensors="pt", padding=True)
        outputs = self._model(**inputs)
        logits_per_image = outputs.logits_per_image
        probs = logits_per_image.softmax(dim=1)
        caption_probs = {}
        for i, caption in enumerate(captions):
            caption_probs[caption] = probs[0][i].item()
        result = CLIPResultObject(image, caption_probs)
        return result

    def process_using_db(self, database_path, limit_images = 10):
        results : dict[str, CLIPResultObject] = {}
        for image_path, surrounding_text in process_images_k_by_k(database_path):
            if len(surrounding_text) == 0 or not os.path.exists(image_path):
                pass
            else:
                print(image_path)
                captions = self.split_text_with_overlap(surrounding_text)
                image = Image.open(image_path)
                results[image_path] = self.assign_probs_caption(image, captions)
                if len(results) > limit_images:
                    break
        return results

    def get_image_and_captions(self, image_id : str):
        image_path, surrounding_text = get_image_captions(image_id)
        if image_id is None or surrounding_text is None :
            raise Exception(f"Image Id {image_id} not found")
        captions = self.split_text_with_overlap(surrounding_text)
        image = Image.open(image_path)
        return image, captions

    def process(self, image_id : str):
        image_path, captions = get_image_captions(image_id)
        image = Image.open(image_path)
        result = self.assign_probs_caption(image, captions)
        return result

    def caption(self, image_id: str) -> str:
        result = self.process(image_id)
        max_prob, best_caption = result.get_best()
        return best_caption