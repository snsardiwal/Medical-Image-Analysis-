import numpy as np


def flood_fill_by_border_color(image_array, start_point, border_color, fill_color):
    """
    Preforms Flood-fill algorithm to fill image region from start_point
    using information about region border color
    :param image_array: Image numpy array of shape (height, width, 3 RGB colors)
    :param start_point: Tuple of shape (x, y)
    :param border_color: Tuple presented a color of region border (red, green, blue)
    :param fill_color: Tuple presented a color for region filling (red, green, blue)
    """
    if np.array_equal(image_array[start_point[1], start_point[0], :], border_color):
        raise ValueError('Color of starting point is equal to border color')

    height, width, _ = image_array.shape
    stack = {(start_point[0], start_point[1])}

    while stack:
        x, y = stack.pop()

        if not np.array_equal(image_array[y, x, :], border_color):
            image_array[y, x, :] = fill_color

            if x > 0:
                stack.add((x - 1, y))
            if x < (width - 1):
                stack.add((x + 1, y))
            if y > 0:
                stack.add((x, y - 1))
            if y < (height - 1):
                stack.add((x, y + 1))
