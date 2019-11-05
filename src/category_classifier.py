import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
import tensorflow as tf
import numpy as np
import cv2 as cv
import json, random
from configs import configs
from embedding import partition

configs = configs['CAT_CLASS']

IMAGE_DIM = (None, None, 3)


def get_output_vec(cat_list, labels):
	cat_ind_list = []
	cat_list = cat_list[configs['cat_lower_limit']:configs['cat_upper_limit']]
	for cat in cat_list:
		if cat in labels:
			cat_ind_list.append(labels.index(cat))
	return cat_ind_list


def load_dataset(source='../dataset/dataset.txt'):
	label_map = {}
	with open(source) as f:
		raw_file = f.readlines()
		random.shuffle(raw_file)
		for record in raw_file:
			data = json.loads(record)
			labels = data['label'][configs['cat_lower_limit']:configs['cat_upper_limit']]  # get only c2
			for label in labels:
				if not label in label_map:
					label_map[label] = 1
				else:
					label_map[label] += 1
	labels = []
	for label, value in label_map.items():
		if value > configs['category_thresh_bucket']:
			labels.append(label)
	return partition(raw_file, configs['batch']), labels


def get_batches_dataset(raw_file, labels, source='../dataset/'):
	images, output = [], []
	for record in raw_file:
		try:
			data = json.loads(record)
			image = cv.imread(source + data['dir'])
			if not image.shape == (380, 380, 3):
				continue
			label = get_output_vec(data['label'], labels)
			output_vec = np.zeros(len(labels))
			output_vec[label] = 1
			output.append(output_vec)
			images.append(image)
		except:
			continue

	images = np.array(images)
	output = np.asarray(output)
	print 'Images: ', images.shape
	print 'Labels: ', output.shape
	print 'Categories: ', len(labels)
	return images, output


def get_model(labels):
	base_model = tf.keras.applications.ResNet50(
		include_top=False,
		weights='imagenet',
		input_shape=IMAGE_DIM,
		pooling=None
	)
	base_model.trainable = False
	global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
	prediction_layer = tf.keras.layers.Dense(len(labels), activation='softmax')
	model = tf.keras.Sequential([
		base_model,
		global_average_layer,
		prediction_layer
	])
	alpha = 0.0001
	model.compile(optimizer=tf.keras.optimizers.RMSprop(lr=alpha),
				  loss='binary_crossentropy',
				  metrics=['accuracy'])
	model.summary()
	return model


def train(input, output, model):
	SPLIT_WEIGHTS = (8, 1, 1)  # train, validation, test
	num_train, num_val, num_test = (len(input) * weight / 10 for weight in SPLIT_WEIGHTS)
	train_set, val_set, test_set = np.split(input, [num_train, num_train + num_val])
	train_label, val_label, test_label = np.split(output, [num_train, num_train + num_val])
	epochs = configs['epochs']
	model.fit(train_set, train_label,
			  epochs=epochs,
			  validation_data=(val_set, val_label))
	return model


def save_model(model, labels):
	tf.keras.experimental.export_saved_model(model, configs['model_path'])
	model.save('../models/catgegory_class.h5')
	with open('../models/cat_label.json', 'w') as f:
		json.dump(labels, f)


try:
	with open('../models/cat_label_gpu.json', 'r') as f:
		cat_label_map = json.load(f)
except:
	print "ERROR Failed loading category labels"
	pass


def get_intent_categories(image):
	tf.compat.v1.InteractiveSession()
	category_classifier = tf.keras.models.load_model('../models/catgegory_class_gpu.h5')
	scores, links = [], []
	global cat_label_map
	for index, score in enumerate(category_classifier.predict(np.array([image]))[0]):
		scores.append([score * 100, index])
	top_cats = sorted(scores, key=lambda x: x[0], reverse=True)[:configs['TOP_CATEGORIES_DETECTED']]
	return [[cat_label_map[index[1]], index[0]] for index in top_cats if index[0] > configs['CATEGORY_THRESH']]


if __name__ == '__main__':
	batches, labels = load_dataset()
	model = get_model(labels)
	for batch in batches:
		print "Processing Next Batch"
		input, output = get_batches_dataset(batch, labels)
		model = train(input, output, model)
		save_model(model, labels)
		del input, output
