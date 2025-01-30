from src.common.ClipSocialModel import CLIPSocialModel

model_path = "../../../external/trained_models/clip_image_captioning_base"
database_path = "sqlite:///../../../external/dataset/metadata.db"

clip = CLIPSocialModel(model_path)
clip.process_using_db(database_path)

results = clip.process_using_db(database_path, limit_images= 3)
for clip_result in results.values():
    clip_result.visualize()