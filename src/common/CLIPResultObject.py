import random
import matplotlib.pyplot as plt
from PIL import Image
from matplotlib.widgets import Slider


class CLIPResultObject:
    def __init__(self, image : Image, caption_probs : dict[str, float]):
        self.image = image
        self.captions_probs = caption_probs
    def visualize(self):
        plot_image_with_captions(self.image, self.captions_probs)

def plot_image_with_captions(image, caption_probs):
    fig, ax = plt.subplots(2, 1, figsize=(12, 12))
    fig.subplots_adjust(left=0.5, bottom=0.2)  # Adjust the left and bottom margins to create more space for labels and slider

    ax[0].imshow(image)
    ax[0].axis('off')

    captions = list(caption_probs.keys())
    probs = list(caption_probs.values())
    colors = [f"#{random.randint(0, 0xFFFFFF):06x}" for _ in probs]

    y_pos = range(len(captions))
    bar_container = ax[1].barh(y_pos, probs, color=colors, edgecolor='k')
    ax[1].set_yticks(y_pos)
    ax[1].set_yticklabels(captions)
    ax[1].invert_yaxis()  # Invert y-axis to have the highest probability on top
    ax[1].set_xlim(0, 1)
    ax[1].set_xlabel("Probability")
    ax[1].set_title("Caption Probabilities")

    # Add a slider for scrolling
    ax_slider = plt.axes([0.1, 0.05, 0.8, 0.03], facecolor='lightgoldenrodyellow')
    slider = Slider(ax_slider, 'Scroll', 0, len(captions) - 1, valinit=0, valstep=1)

    def update(val):
        pos = slider.val
        ax[1].set_ylim(pos - 5, pos + 5)  # Adjust the range to show 10 items at a time
        fig.canvas.draw_idle()

    slider.on_changed(update)
    plt.show()