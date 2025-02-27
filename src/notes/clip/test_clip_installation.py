import requests
from transformers import CLIPProcessor, CLIPModel
from PIL import Image

model1 = "../../../external/trained_models/clip_image_captioning_base"
model2 = "../../../external/trained_models/clip_image_captioning_base2"

model = CLIPModel.from_pretrained(model2)

processor = CLIPProcessor.from_pretrained(model2)

url = "http://images.cocodataset.org/val2017/000000039769.jpg"
image = Image.open(requests.get(url, stream=True).raw)

inputs = processor(text=["two cats", "three cats"], images=image, return_tensors="pt", padding=True)

outputs = model(**inputs)
logits_per_image = outputs.logits_per_image # this is the image-text similarity score
probs = logits_per_image.softmax(dim=1) # we can take the softmax to get the label probabilities
print(probs)