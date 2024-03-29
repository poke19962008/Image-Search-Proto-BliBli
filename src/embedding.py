import tensorflow as tf
from configs import configs
import cv2 as cv
import requests
import numpy as np

IMAGE_DIM = (380, 380, 3)


def get_embedding(image_np):
	if configs['TFX']:
		payload = {
			'instances': np.array([image_np]).tolist()
		}
		data = requests.post(configs['EMBEDDING_TFX_HOST'] + '/v1/models/embedding:predict', json=payload)
		return np.array(data.json()['predictions'][0])
	else:
		tf.compat.v1.InteractiveSession()
		base_model = tf.keras.applications.ResNet50(weights='imagenet', pooling=max, include_top=False)
		global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
		model = tf.keras.Sequential([
			base_model,
			global_average_layer
		])
		feature = model.predict(np.array([image_np]))
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
	model = tf.keras.Sequential([
		base_model,
		global_average_layer
	])
	tf.keras.experimental.export_saved_model(model, configs['EMBEDDING_MODEL'])
