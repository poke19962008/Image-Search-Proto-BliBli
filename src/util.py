import tensorflow as tf
import cv2 as cv

IMAGE_DIM = (380, 380, 3)

def get_embedding(image_np, flatten=False):
	sess = tf.InteractiveSession()
	model = tf.keras.applications.ResNet50(weights='imagenet', pooling=max, include_top=False)
	global_average_layer = tf.keras.layers.GlobalAveragePooling2D()

	feature = model.predict(image_np.reshape((1, 380, 380, 3)))
	if flatten:
		feature = tf.reshape(tf.squeeze(feature), [-1])
	else:
		feature = global_average_layer(feature)
		feature = tf.squeeze(feature)

	return feature.eval()


def partition(l, n):
	"""Yield successive n-sized chunks from l."""
	for i in range(0, len(l), n):
		yield l[i:i + n]


def read_image(url):
	return cv.imread(url)
