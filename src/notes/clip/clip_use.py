from src.common.ClipSocialModel import CLIPSocialModel
import random as rd

model_path = "../../../external/trained_models/clip_image_captioning_base2"
database_path = "sqlite:///../../../external/dataset/metadata.db"

clip = CLIPSocialModel(model_path)
clip.process_using_db(database_path)

results = clip.results

random_values = rd.sample(list(results.values()), 10)

# Print the selected random values
for value in random_values:
    value.visualize()