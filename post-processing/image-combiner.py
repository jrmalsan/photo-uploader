import copy
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

THRESHOLD = 30
PERCENTAGE = 0.1
FOLDER = '../pictures/second_test'

def closed_mask_background(background, images):
    """Combines the differences between each image and the background by 
        substituting the pixels from each successive image that deviated
        by more than THRESHOLD DN in total across the colors. Adds images in order
        of list index so the last image is the top layer.
    Inputs:
        background: np array, image of the background to be removed
        images:list of np array, list of images to be merged
    Outputs:
        merged: np array, merged image
    """
    masked = copy.copy(background)
    counter = 0 
    for image in images:
        diff = np.abs(image.astype(np.float) - background.astype(np.float))
        percentage = np.sum(diff, axis=2) / np.sum(background, axis=2)
        mask = percentage > PERCENTAGE
        Image.fromarray((mask*255).astype(np.uint8)).save('{}/mask{}.png'.format(FOLDER, counter))
        masked[percentage > PERCENTAGE] = image[percentage > PERCENTAGE, :]
        counter += 1
    
    return masked

def percentage_mask_background(background, images):
    """Combines the differences between each image and the background by 
        substituting the pixels from each successive image that deviated
        by more than PERCENTAGE of the initial image. Adds images in order
        of list index so the last image is the top layer.
    Inputs:
        background: np array, image of the background to be removed
        images:list of np array, list of images to be merged
    Outputs:
        merged: np array, merged image
    """
    masked = copy.copy(background)
    counter = 0 
    for image in images:
        diff = np.abs(image.astype(np.float) - background.astype(np.float))
        percentage = np.sum(diff, axis=2) / np.sum(background, axis=2)
        mask = percentage > PERCENTAGE
        Image.fromarray((mask*255).astype(np.uint8)).save('{}/mask{}.png'.format(FOLDER, counter))
        masked[percentage > PERCENTAGE] = image[percentage > PERCENTAGE, :]
        counter += 1
    
    return masked

def simple_mask_background(background, images):
    """Combines the differences between each image and the background by 
        substituting the pixels from each successive image that deviated
        by more than THRESHOLD DN in total across the colors. Adds images in order
        of list index so the last image is the top layer.
    Inputs:
        background: np array, image of the background to be removed
        images:list of np array, list of images to be merged
    Outputs:
        merged: np array, merged image
    """
    masked = copy.copy(background)
    
    for image in images:
        diff = np.abs(image.astype(np.float) - background.astype(np.float))
        diff = np.sum(diff, axis=2)
        masked[diff > THRESHOLD] = image[diff > THRESHOLD, :]
    
    return masked

def subtract_background(background, images):
    """Combines the differences of images 1 and 2 by subtracting the background
        from the sum of the list of images
    Inputs:
        background: np array, image of the background to be removed
        images:list of np array, list of images to be merged
    Outputs:
        merged: np array, merged image
    """
    plt.imshow(background)
    plt.show(block=True)
    merged = 0 - background.astype(np.float) * (len(images) - 1)

    for image in images:
        plt.imshow(image)
        plt.show(block=True)
        merged += image.astype(np.float)

    merged[merged < 0] = 0
    merged[merged > 255] = 255
    merged = merged.astype(np.uint8)

    return merged

def image_loader(folder, name_root):
    """Loads the first image in the folder as background and the rest 
        get put into the image list images
    Inputs:
        folder: string, path to the folder of test images
        name_root: string, substring that must be in the picture name
    Outputs:
        background: np array, first image taken in the folder
        images: list of np arrays, remaining images in the folder
    """
    if not os.path.isdir(folder):
        print('{} is not a valid folder'.format(folder))
        return np.zeros((10, 10, 3)), []
    
    files = os.listdir(folder)
    valid_files = [fil for fil in files if fil.find(name_root) != -1]
    valid_files.sort()

    if len(valid_files) == 0:
        print('No files with name containing {} present in {}'.format(name_root, folder))
        return np.zeros((10, 10, 3)), []

    background = np.array(Image.open('{}/{}'.format(folder, valid_files[0])))
    images = []
    for image_file in valid_files[1:]:
        images.append(np.array(Image.open('{}/{}'.format(folder, image_file))))
    
    return background, images


def main():
    background, images = image_loader(FOLDER, 'pi-capture')
    
    merged = subtract_background(background, images)
    merged_image = Image.fromarray(merged)
    merged_image.save('{}/subtracted.png'.format(FOLDER))

    masked = simple_mask_background(background, images)

    masked_image =  Image.fromarray(masked)
    masked_image.save('{}/simple_masked.png'.format(FOLDER))

    masked = percentage_mask_background(background, images)

    masked_image =  Image.fromarray(masked)
    masked_image.save('{}/percentage_masked.png'.format(FOLDER))

if __name__ == "__main__":
    main()