from transformers import CLIPProcessor, CLIPModel

model1 = "openai/clip-vit-base-patch32"
model2 = "openai/clip-vit-large-patch14"

model = CLIPModel.from_pretrained(model2)
processor = CLIPProcessor.from_pretrained(model2)

# Save the model and processor locally
processor.save_pretrained("../../../external/trained_models/clip_image_captioning_base2")
model.save_pretrained("../../../external/trained_models/clip_image_captioning_base2")