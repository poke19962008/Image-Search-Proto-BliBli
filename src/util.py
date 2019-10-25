import tensorflow as tf
import cv2 as cv

sess = tf.InteractiveSession()
IMAGE_DIM = (380, 380, 3)
model = tf.keras.applications.ResNet50(weights='imagenet', pooling=max, include_top=False)
global_average_layer = tf.keras.layers.GlobalAveragePooling2D()


def get_embedding(image_np, flatten=False):
	feature = model.predict(image_np.reshape((1, 380, 380, 3)))
	if flatten:
		feature = tf.reshape(tf.squeeze(feature), [-1])
	else:
		feature = global_average_layer(feature)
		feature = tf.squeeze(feature)

	return feature.eval()


def read_image(url):
	return cv.imread(url)
