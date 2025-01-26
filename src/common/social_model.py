from abc import ABC, abstractmethod
from PIL import ImageFile
from transformers import BlipProcessor, BlipForConditionalGeneration
import lorem

class SocialModel(ABC):
    @abstractmethod
    def caption(raw_image : ImageFile.ImageFile) -> str:
        pass

class BLIP_SocialModel(SocialModel):
    def __init__(self, path : str):
        self._processor = BlipProcessor.from_pretrained(path)
        self._model = BlipForConditionalGeneration.from_pretrained(path)
    
    def caption(self, raw_image : ImageFile.ImageFile):
        inputs = self._processor(images=raw_image, return_tensors="pt")
        outputs = self._model.generate(**inputs, num_beams=1, max_length=40)
        return self._processor.decode(outputs[0], skip_special_tokens=True)
    
class Random_SocialModel(SocialModel):
    def caption(self, raw_image):
        return lorem.sentence()