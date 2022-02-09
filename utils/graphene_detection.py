#!/usr/bin/env python
## Object Detection From TF2 Saved Model
# coding: utf-8
""" This file will detect graphene and record the location
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'    # Suppress TensorFlow logging (1)
import pathlib
import tensorflow as tf

tf.get_logger().setLevel('ERROR')           # Suppress TensorFlow logging (2)

# Enable GPU dynamic memory allocation
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)


# Load the model
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import time
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils

PATH_TO_MODEL_DIR = str(pathlib.Path.cwd() / 'my_model_centernet')
PATH_TO_SAVED_MODEL = PATH_TO_MODEL_DIR + "/saved_model"

print('Loading model...', end='')
start_time = time.time()

# Load saved model and build the detection function
detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)

end_time = time.time()
elapsed_time = end_time - start_time
print('Done! Took {} seconds'.format(elapsed_time))


# Load label map data (for plotting)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Label maps correspond index numbers to category names, so that when our convolution network
# predicts `5`, we know that this corresponds to `airplane`.  Here we use internal utility
# functions, but anything that returns a dictionary mapping integers to appropriate string labels
# would be fine.
PATH_TO_LABELS = str(pathlib.Path.cwd() / 'label_map.pbtxt')
category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS,
                                                                    use_display_name=True)


# Putting everything together
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The code shown below loads an image, runs it through the detection model and visualizes the
# detection results, including the keypoints.
#
# Note that this will take a long time (several minutes) the first time you run this code due to
# tf.function's trace-compilation --- on subsequent runs (e.g. on new images), things will be
# faster.
#
# Here are some simple things to try out if you are curious:
#
# * Modify some of the input images and see if detection still works. Some simple things to try out here (just uncomment the relevant portions of code) include flipping the image horizontally, or converting to grayscale (note that we still expect the input image to have 3 channels).
# * Print out `detections['detection_boxes']` and try to match the box locations to the boxes in the image.  Notice that coordinates are given in normalized form (i.e., in the interval [0, 1]).
# * Set ``min_score_thresh`` to other values (between 0 and 1) to allow more detections in or to filter out more detections.
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import shutil
import warnings
warnings.filterwarnings('ignore')   # Suppress Matplotlib warnings

def load_image_into_numpy_array(path):
    """Load an image from file into a numpy array.

    Puts image into numpy array to feed into tensorflow graph.
    Note that by convention we put it into a numpy array with shape
    (height, width, channels), where channels=3 for RGB.

    Args:
      path: the file path to the image

    Returns:
      uint8 numpy array with shape (img_height, img_width, 3)
    """
    return np.array(Image.open(path))

def detect(folder_name, RESULT_PATH, main_coor, probability=0.7, flip_horizontally=False, grayscale=False, not_photo=1):
  # Count the number of photos
  FOLDER_PATH = str(pathlib.Path.cwd() / folder_name)
  num_file = len([name for name in os.listdir(FOLDER_PATH) if os.path.isfile(os.path.join(FOLDER_PATH, name))])-not_photo
  IMAGE_PATHS = [f'{FOLDER_PATH}/{i}.png' for i in range(num_file)]

  for n,image_path in enumerate(IMAGE_PATHS):

      print('Running inference for {}... '.format(image_path), end='')

      image_np = load_image_into_numpy_array(image_path)

      # Things to try:
      if flip_horizontally:
        image_np = np.fliplr(image_np).copy()
        
      # Convert image to grayscale
      if grayscale:
        image_np = np.tile(np.mean(image_np, 2, keepdims=True), (1, 1, 3)).astype(np.uint8)

      # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
      input_tensor = tf.convert_to_tensor(image_np)
      # The model expects a batch of images, so add an axis with `tf.newaxis`.
      input_tensor = input_tensor[tf.newaxis, ...]

      # input_tensor = np.expand_dims(image_np, 0)
      detections = detect_fn(input_tensor)

      # All outputs are batches tensors.
      # Convert to numpy arrays, and take index [0] to remove the batch dimension.
      # We're only interested in the first num_detections.
      num_detections = int(detections.pop('num_detections'))
      need_detection_key = ['detection_classes','detection_boxes','detection_masks','detection_scores']
      detections = {key: detections[key][0, :num_detections].numpy()
                    for key in need_detection_key}
      detections['num_detections'] = num_detections

      # detection_classes should be ints.
      detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

      image_np_with_detections = image_np.copy()

      viz_utils.visualize_boxes_and_labels_on_image_array(
            image_np_with_detections,
            detections['detection_boxes'],
            detections['detection_classes'],
            detections['detection_scores'],
            category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=20,
            min_score_thresh=.30,
            agnostic_mode=False)

      print('Done')

      print('Probability: ', detections['detection_scores'][0])
      if detections['detection_scores'][0] > probability:
        print('getcha!')
        plt.figure()
        plt.imshow(image_np_with_detections)
        # save photos
        plt.savefig(f'{RESULT_PATH}/{n}d.png')
        shutil.copyfile(f'{FOLDER_PATH}/{n}.png', f'{RESULT_PATH}/{n}.png')
        # Write info to a txt
        f = open(f'{RESULT_PATH}/Log file.txt', 'a')
        f.write(f'\n{n}.png\t({main_coor.iloc[n][0]}, {main_coor.iloc[n][1]})')
        f.close()
  plt.show()
