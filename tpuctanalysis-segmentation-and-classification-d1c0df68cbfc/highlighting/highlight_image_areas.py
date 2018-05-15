import numpy as np

from PIL import Image
from .masking import get_probability_mask
from config.highlighting_config import tissue_highlighting_options as th_opt
from config.highlighting_config import probability_highlighting_options as ph_opt


def highlight_probas_on_preset_slice(slice_image_data, probabilities, coordinates):
    """
    Performs highlighting of certain points on the preset slice
    according to probability values
    :param slice_image_data: Numpy array of image slice of shape (height, width)
    :param probabilities: Numpy array of probabilities of shape (probability number,)
    :param coordinates: Numpy array of tuples of coordinates of shape (x, y).
    Each position of coordinates value corresponds to the position of probability value
    :return: Pillow image object in RGBA format
    """
    slice_image = Image.fromarray(slice_image_data).convert('RGBA')

    color_mask = ph_opt['color_masks'][1]
    probability_mask = get_probability_mask(slice_image_data.shape[0],
                                            slice_image_data.shape[1],
                                            probabilities,
                                            coordinates)
    highlighting_mask = __create_highlighting_mask(probability_mask, color_mask)
    highlighting_mask = (highlighting_mask * 255).astype(np.uint8)
    highlighting_img = Image.fromarray(highlighting_mask)

    slice_image.paste(highlighting_img, box=None, mask=highlighting_img)

    return slice_image


def highlight_mask_on_preset_slices(slices_image_data, masks):
    """
    Performs highlighting all the areas encoded in masks array
    on the each slice of slices_image_data array
    :param slices_image_data: Numpy array of slices converted to a certain preset
    :param masks: Masks to highlight areas on a slice image
    :return: List of PIL Image objects - highlighted slice images
    """
    color_masks = __create_color_masks(len(masks))
    if len(color_masks) < len(masks):
        print('Warning: not all the areas will be highlighted'
              'due to lack of available colors')

    highlighted_slice_images = []
    for i in range(slices_image_data.shape[0]):
        # Convert slice image data to RGBA image
        slice_image = Image.fromarray(slices_image_data[i]).convert('RGBA')
        slice_image_array = np.array(slice_image)

        # Perform highlighting the areas according to all the masks
        for j in range(len(masks)):
            # Obtain highlighted area of the slice image
            highlighting_mask = __create_highlighting_mask(masks[j][i], color_masks[j])
            masked_slice_image_array = \
                (slice_image_array * highlighting_mask).astype(np.uint8)
            masked_slice_image = Image.fromarray(masked_slice_image_array)

            # Insert highlighted area to the slice image
            slice_image.paste(masked_slice_image, box=None, mask=masked_slice_image)

        highlighted_slice_images.append(slice_image)

    return highlighted_slice_images


def __create_color_masks(count):
    """
    Loads color masks from the config.
    If number of available colors is lower than requested count
    then only the available colors are loading
    :param count: Requested number of colors to load
    :return: List of colors, each item is a list with shape [R, G, B, A]
    """
    available_colors = th_opt['color_masks']
    num_masks_to_load = min(len(available_colors), count)

    return available_colors[:num_masks_to_load]


def __create_highlighting_mask(image_mask, color_mask):
    """
    Creates the colored masks as a numpy array with RGBA data
    :param image_mask: Mask to highlight areas on an image
    :param color_mask: Mask for color representation
    :return: Colored image mask as a numpy array
    """
    red_channel = np.expand_dims(image_mask, axis=2)
    green_channel = np.expand_dims(image_mask, axis=2)
    blue_channel = np.expand_dims(image_mask, axis=2)
    alpha_channel = np.expand_dims(image_mask, axis=2)
    ready_image_mask = np.concatenate((red_channel,
                                       green_channel,
                                       blue_channel,
                                       alpha_channel), axis=2)

    return ready_image_mask * color_mask
