import argparse
import numpy as np
import os

from PIL import Image
from tqdm import tqdm
from class_labels_working import get_label_mask_regions_with_seed
from class_labels_working import get_label_mask_polygons
from config.labels_config import label_options as l_opt


def create_label_masks_for_images(images_contained_folder,
                                  label_presentation_mode,
                                  major_color,
                                  minor_color,
                                  label_name,
                                  output_folder,
                                  verbose=False):
    """
    Creates binary label masks for each image in the images_contained_folder
    :param images_contained_folder: Path to the folder contained images
    :param label_presentation_mode: String to define mode of label representation
    on the each image in the folder: regions or polygons
    :param major_color: First color for region border or polygon color representation
    :param minor_color: Second color for representation color of a seed inside the region
    :param label_name: String to define class label representation
    :param output_folder: Path to the folder to save binary label masks as NPY files
    :param verbose: Whether to show progress report
    """
    # Check the arguments validity
    if major_color not in l_opt['colors'] or minor_color not in l_opt['colors']:
        raise AttributeError('One of selected colors is incorrect. '
                             'There is no such a color in the config file.')
    first_color = l_opt['colors'][major_color]
    second_color = l_opt['colors'][minor_color]

    if label_name not in l_opt['names']:
        raise AttributeError('Label name is incorrect. '
                             'There is no such a label name in the config file.')
    label = l_opt['names'][label_name]

    # Read image file names from the folder
    file_names = sorted(os.listdir(images_contained_folder))
    image_names = []
    for fn in file_names:
        file_extension = fn.split('.')[-1]
        if file_extension in l_opt['image_options']['file_extensions']:
            image_names.append(fn)

    # If no one image is found then exit
    if len(image_names) == 0:
        print('Images are not found')
        return

    # Create console progress bar if it is defined
    progress_bar = None
    if verbose:
        print('Processing images from \'{}\' folder...'.format(images_contained_folder))
        progress_bar = tqdm(total=len(image_names))

    # Load images, create label masks and save them
    for img_name in image_names:
        img_path = os.path.join(images_contained_folder, img_name)
        img = Image.open(img_path).convert('RGB')
        img_array = np.array(img)

        if label_presentation_mode == 'regions':
            label_mask = get_label_mask_regions_with_seed(img_array,
                                                          first_color,
                                                          second_color,
                                                          label)
        elif label_presentation_mode == 'polygons':
            label_mask = get_label_mask_polygons(img_array, first_color, label)
        else:
            raise AttributeError('Unknown mode for label representation')

        img_name_without_ext = img_name.split('.')[0]
        binary_file_path = os.path.join(output_folder, img_name_without_ext)
        np.save(binary_file_path, label_mask)

        if verbose:
            progress_bar.update(1)

    if verbose:
        progress_bar.close()


def main(images_contained_folder,
         label_presentation_mode,
         major_color,
         minor_color,
         label_name,
         output_folder,
         verbose):
    create_label_masks_for_images(images_contained_folder,
                                  label_presentation_mode,
                                  major_color,
                                  minor_color,
                                  label_name,
                                  output_folder,
                                  verbose=verbose)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Reads label images from folder '
                                                 'and creates label masks')

    parser.add_argument(
        '-i',
        '--input_folder',
        help='Path to the folder contained label images'
    )

    parser.add_argument(
        '-m',
        '--mode',
        help='Set a mode for label representation. One of the following:'
             'regions, polygons. Default is regions',
        default='regions'
    )

    parser.add_argument(
        '-c',
        '--color',
        help='Set a color for borders (regions mode) or polygons (polygons mode).'
             'All the colors can be set in config/labels_config.py file.'
             'You should set a name of color as in the config file. '
             'Default is \'ms_paint_red\'',
        default='ms_paint_red'
    )

    parser.add_argument(
        '-s',
        '--seed_color',
        help='Set a color for region seed (pixel color in the region in regions mode).'
             'All the colors can be set in config/labels_config.py file.'
             'You should set a name of color as in the config file. '
             'Default is \'ms_paint_green\'',
        default='ms_paint_green'
    )

    parser.add_argument(
        '-l',
        '--label_name',
        help='Class label name to create a mask.'
             'All the label names can be set in config/labels_config.py file.'
             'You should set a name of class label as in the config file.'
             'Default is \'disseminated\'',
        default='disseminated'
    )

    parser.add_argument(
        '-o',
        '--output_folder',
        help='Path to the folder to save label masks'
    )

    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Whether to show progress report in the console. Default is False',
        default=False
    )

    args = parser.parse_args()

    main(args.input_folder,
         args.mode,
         args.color,
         args.seed_color,
         args.label_name,
         args.output_folder,
         args.verbose)
