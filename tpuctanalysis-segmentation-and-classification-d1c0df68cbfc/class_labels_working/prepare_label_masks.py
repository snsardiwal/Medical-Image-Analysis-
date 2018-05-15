import numpy as np

from utils import flood_fill_by_border_color


def get_label_mask_regions_with_seed(image_array,
                                     border_color,
                                     seed_color,
                                     label=1):
    """
    Obtains label mask from image array with bordered regions -
    areas contained objects of a certain class
    :param image_array: Image numpy array of shape (height, width, 3 RGB colors)
    :param border_color: Tuple presented a color of region border (red, green, blue)
    :param seed_color: Tuple presented a color of a seed inside regions (red, green, blue)
    :param label: Number for label mask to encode class objects
    :return: Numpy array of label mask of shape (height, width)
    """
    polygon_image_array = __fill_label_region_with_seed(image_array,
                                                        border_color,
                                                        seed_color,
                                                        border_color)

    label_mask = __get_label_mask(polygon_image_array, border_color, label)
    return label_mask


def get_label_mask_polygons(image_array, polygon_color, label=1):
    """
    Obtains label mask from image array with polygons -
    areas contained objects of a certain class
    :param image_array: Image numpy array of shape (height, width, 3 RGB colors)
    :param polygon_color: Tuple presented a color of polygons (red, green, blue)
    :param label: Number for label mask to encode class objects
    :return: Numpy array of label mask of shape (height, width)
    """
    label_mask = __get_label_mask(image_array, polygon_color, label)
    return label_mask


def __fill_label_region_with_seed(image_array, border_color, seed_color, fill_color):
    """
    Performs flood filling of regions with border and seed of a certain color
    :param image_array: Image numpy array of shape (height, width, 3 RGB colors)
    :param border_color: Tuple presented a color of region border (red, green, blue)
    :param seed_color: Tuple presented a color of a seed inside regions (red, green, blue)
    :param fill_color: Tuple presented a color for region filling (red, green, blue)
    :return: Image numpy array with filled regions (polygons) of shape
    (height, width, 3 RGB colors)
    """
    filled_image_array = np.copy(image_array)
    height, width, _ = filled_image_array.shape

    # Fill regions with a certain color
    for y in range(height):
        for x in range(width):
            if np.array_equal(filled_image_array[y, x, :], seed_color):
                flood_fill_by_border_color(filled_image_array,
                                           (x, y),
                                           border_color,
                                           fill_color)

    return filled_image_array


def __get_label_mask(polygon_image_array, polygon_color, label):
    """
    Creates label mask based on the image array contained areas
    of a certain color called polygons
    :param polygon_image_array: Image numpy array of shape (height, width, 3 RGB colors)
    :param polygon_color: Tuple presented a color of the polygons of the image
    (red, green, blue)
    :param label: Number for label mask to encode class objects
    :return: Numpy array of label mask of shape (height, width)
    """
    height, width, _ = polygon_image_array.shape
    label_mask = np.zeros((height, width, 1), )

    # Fill label mask by a certain number
    for y in range(height):
        for x in range(width):
            if np.array_equal(polygon_image_array[y, x, :], polygon_color):
                label_mask[y, x, :] = label

    label_mask = np.reshape(label_mask, (label_mask.shape[0], label_mask.shape[1]))
    return label_mask.astype(np.uint8)
