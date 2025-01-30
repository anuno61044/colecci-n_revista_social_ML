import requests
from PIL import Image

from src.common.ClipSocialModel import CLIPSocialModel

model1 = "../../../external/trained_models/clip_image_captioning_base"
model2 = "../../../external/trained_models/clip_image_captioning_base2"

url = "http://images.cocodataset.org/val2017/000000039769.jpg"
image = Image.open(requests.get(url, stream=True).raw)
captions = [
    "two TV remote controls",
    "two cats sleeping",
    "two cats and two laptops on a sofa"
]

clip = CLIPSocialModel(model2)
result = clip.assign_probs_caption(image, captions)
result.visualize()