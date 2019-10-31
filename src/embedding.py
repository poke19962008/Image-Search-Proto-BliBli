import tensorflow as tf
from configs import configs
import cv2 as cv

IMAGE_DIM = (380, 380, 3)

def get_embedding(image_np):
	tf.InteractiveSession()
	model = tf.keras.applications.ResNet50(weights='imagenet', pooling=max, include_top=False)
	global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
	feature = model.predict(image_np.reshape((1, 380, 380, 3)))
	feature = global_average_layer(feature)
	feature = tf.squeeze(feature)
	return feature.eval()


def partition(l, n):
	"""Yield successive n-sized chunks from l."""
	for i in range(0, len(l), n):
		yield l[i:i + n]


def read_image(url):
	return cv.imread(url)


if __name__ == '__main__':
	tf.compat.v1.InteractiveSession()
	base_model = tf.keras.applications.ResNet50(weights='imagenet', pooling=max, include_top=False)
	global_average_layer = tf.keras.layers.GlobalAveragePooling2D()

	model = tf.keras.Sequential([
		base_model,
		global_average_layer
	])
	tf.keras.experimental.export_saved_model(model, configs['EMBEDDING_MODEL'])
