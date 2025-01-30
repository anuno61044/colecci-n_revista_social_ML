class CLIPResultObject:
    def __init__(self, image_path : str, caption_probs : dict[str, float]):
        self.image_path = image_path
        self.captions_probs = caption_probs

    def __str__(self):
        result = f"The Image with path {self.image_path} has this captions:\n"
        for caption in self.captions_probs:
            result += f" {caption} with probability = {self.captions_probs[caption]} \n"
        return result