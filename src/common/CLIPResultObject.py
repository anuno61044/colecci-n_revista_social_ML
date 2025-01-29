import matplotlib.pyplot as plt
from PIL import Image

class CLIPResultObject:
    def __init__(self, image_path : str, caption_probs : dict[str, float]):
        self.image_path = image_path
        self.captions_probs = caption_probs

    def __str__(self):
        result = f"The Image with path {self.image_path} has this captions:\n"
        for caption in self.captions_probs:
            result += f" {caption} with probability = {self.captions_probs[caption]} \n"
        return result

    def visualize(self):
        image = Image.open(self.image_path)
        fig, ax = plt.subplots()
        ax.imshow(image)
        ax.axis("off")

        for i, (caption, prob) in enumerate(self.captions_probs.items()):
            ax.text(
                10,
                30 + i * 20,
                f"{caption} : {prob:.2f}:",
                color = "white",
                fontsize = 12,
                bbox = dict(facecolor = "black", alpha = 0.5))
        plt.show()