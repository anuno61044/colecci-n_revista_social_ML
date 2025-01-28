from abc import ABC, abstractmethod
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import lorem

class SocialModel(ABC):
    @abstractmethod
    def caption(self, str : str) -> str:
        pass

class BLIP_SocialModel(SocialModel):
    def __init__(self, path : str):
        self._processor = BlipProcessor.from_pretrained(path)
        self._model = BlipForConditionalGeneration.from_pretrained(path)
    
    def caption(self, image_path : str):
        raw_image = Image.open(image_path).convert('RGB')
        inputs = self._processor(images=raw_image, return_tensors="pt")
        outputs = self._model.generate(**inputs, num_beams=1, max_length=40)
        return self._processor.decode(outputs[0], skip_special_tokens=True)
    
class Random_SocialModel(SocialModel):
    def caption(self, image_path):
        return lorem.sentence()
    

def get_blip():
    return BLIP_SocialModel('../../external/trained_models/blip_image_captioning_base')

def get_tuned_blip():
    return BLIP_SocialModel('../../external/trained_models/blip_image_captioning_tuned')

def get_clip():
    pass

def get_tuned_clip():
    pass

def get_combined_1():
    pass

def get_combined_2():
    pass