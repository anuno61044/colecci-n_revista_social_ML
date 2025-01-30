from src.common.ClipSocialModel import CLIPSocialModel
from src.common.social_model import SocialModel, BLIP_SocialModel

_use_blip_in_clip = 1
_use_max_blip_clip = 2


class BlipAndClipSocialModel(SocialModel):
    def __init__(self, path_blip, path_clip, caption_method=_use_blip_in_clip):
        self.blip_social_model = BLIP_SocialModel(path_blip)
        self.clip_social_model = CLIPSocialModel(path_clip)
        self.caption_method = caption_method

    def max_blip_clip(self, image_id, threshold=0.6):
        blip_result = self.blip_social_model.caption(image_id)
        clip_result = self.clip_social_model.process(image_id)
        if max(clip_result.captions_probs.values()) >= threshold:
            return max(clip_result.captions_probs, key=clip_result.captions_probs.get)
        else:
            return blip_result

    def use_blip_in_clip(self, image_id):
        blip_result = self.blip_social_model.caption(image_id)
        image, captions = self.clip_social_model.get_image_and_captions(image_id)
        captions.append(blip_result)
        clip_result = self.clip_social_model.assign_probs_caption(image, captions)
        return max(clip_result.captions_probs, key=clip_result.captions_probs.get)

    def caption(self, image_id: str) -> str:
        if self.caption_method == _use_blip_in_clip:
            return self.use_blip_in_clip(image_id)
        elif self.caption_method == _use_max_blip_clip:
            return self.max_blip_clip(image_id)
        else:
            raise Exception("Provide a valid method to choose caption")