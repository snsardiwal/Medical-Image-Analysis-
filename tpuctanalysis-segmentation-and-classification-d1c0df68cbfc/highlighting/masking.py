import numpy as np


def get_probability_mask(height, width, probabilities, coordinates):
    """
    Creates a mask with probability values for the items with the certain coordinates
    :param height: Height of the map
    :param width: Width of the map
    :param probabilities: Numpy array of probabilities of shape (probability number,)
    :param coordinates: Numpy array of tuples of coordinates of shape (x, y).
    Each position of coordinates value corresponds to the position of probability value
    :return: Numpy array represents a mask
    """
    mask = np.zeros((height, width), dtype=np.float64)
    for i, coord in enumerate(coordinates):
        mask[coord[1], coord[0]] = probabilities[i]

    return mask
