import tensorflow as tf
import numpy as np
import tarfile, os
from PIL import Image
from object_detection.utils import label_map_util
import cv2 as cv

# What model to download.
# Models can bee found here: https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md
MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('../data', 'mscoco_label_map.pbtxt')

tar_file = tarfile.open('../' + MODEL_FILE)
for file in tar_file.getmembers():
	file_name = os.path.basename(file.name)
	if 'frozen_inference_graph.pb' in file_name:
		tar_file.extract(file, os.getcwd())

detection_graph = tf.Graph()
with detection_graph.as_default():
	od_graph_def = tf.GraphDef()
	with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
		serialized_graph = fid.read()
		od_graph_def.ParseFromString(serialized_graph)
		tf.import_graph_def(od_graph_def, name='')

# Number of classes to detect
NUM_CLASSES = 90
# Loading label map Label maps map indices to category names, so that when our convolution network predicts `5`,
# we know that this corresponds to `airplane`.  Here we use internal utility functions, but anything that returns a
# dictionary mapping integers to appropriate string labels would be fine
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(
	label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)


def load_image_into_numpy_array(image):
	(im_width, im_height) = image.size
	return np.array(image.getdata()).reshape(
		(im_height, im_width, 3)).astype(np.uint8)


def detect_object(image_url):
	image, boxes, scores = [], [], []
	with detection_graph.as_default():
		with tf.Session(graph=detection_graph) as sess:
			global image_np, boxes, scores
			image_np = cv.imread(image_url)
			image_np_expanded = np.expand_dims(image_np, axis=0)
			# Extract image tensor
			image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
			# Extract detection boxes
			boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
			# Extract detection scores
			scores = detection_graph.get_tensor_by_name('detection_scores:0')
			# Extract detection classes
			classes = detection_graph.get_tensor_by_name('detection_classes:0')
			# Extract number of detectionsd
			num_detections = detection_graph.get_tensor_by_name('num_detections:0')
			# Actual detection.
			(boxes, scores, classes, num_detections) = sess.run(
				[boxes, scores, classes, num_detections],
				feed_dict={image_tensor: image_np_expanded})
			score_thresh = .5
			height, width, rgb = image_np.shape
			objects = []
			for box in boxes[scores > score_thresh]:
				image_ = cv.imread(image_url)
				image_pil = Image.fromarray(np.uint8(image_)).convert('RGB')
				ymin, xmin, ymax, xmax = box
				(left, right, top, bottom) = (xmin * width, xmax * width,
											  ymin * height, ymax * height)

				image_pil = image_pil.crop((left, top, right, bottom))
				objects.append(np.array(image_pil))
				return np.array(objects)


if __name__ == '__main__':
	print detect_object('../test/sample2.jpg')
