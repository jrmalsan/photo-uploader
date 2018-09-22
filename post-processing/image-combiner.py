import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def combine_images(background, image_1, image_2):
    """Combines the differences of images 1 and 2
    Inputs:
        background: np array, image of the background to be removed
        image_1: np array, first image to be merged
        image_2: np array, second image to be merged
    Outputs:
        merged: np array, merged image
    """
    background = background.astype(np.float)
    image_1 = image_1.astype(np.float)
    image_2 = image_2.astype(np.float)

    merged = image_1 + image_2 - background
    merged[merged < 0] = 0
    merged[merged > 255] = 255
    merged = merged.astype(np.uint8)

    return merged

def main():
    background_image = '../pictures/pi-capture-1537645048.png'
    image_1_name = '../pictures/pi-capture-1537645150.png'
    image_2_name = '../pictures/pi-capture-1537645173.png'

    background = np.array(Image.open(background_image))
    image_1 = np.array(Image.open(image_1_name))
    image_2 = np.array(Image.open(image_2_name))

    merged = combine_images(background, image_1, image_2)

    plt.imshow(merged)
    plt.show(block=True)

    merged_image = Image.fromarray(merged)
    merged_image.save('../pictures/merged.png')

if __name__ == "__main__":
    main()