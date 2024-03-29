from embedding import get_embedding, read_image
from category_classifier import get_intent_categories
from tf_object_detection import detect_object
from configs import configs
from matplotlib import pyplot as plt
import cv2 as cv
import requests, timeit
import matplotlib

HOST = configs['SOLR_HOST']
COLL = configs['SOLR_COLL']
url = 'http://' + HOST + '/solr/' + COLL


def search_by_image(image_np):
	flip_horizontal = cv.flip(image_np, 1)
	aug_images = [image_np, flip_horizontal]

	results = []
	total_cats = []
	for images in aug_images:
		start = timeit.default_timer()
		vec = get_embedding(images)
		stop = timeit.default_timer()
		print "Time to load vectors=", stop - start
		start = timeit.default_timer()
		cats = get_intent_categories(images)
		stop = timeit.default_timer()
		print "Time to load categories=", stop - start
		total_cats += cats
		cat_codes = [cat[0] for cat in cats]
		start = timeit.default_timer()
		results += query_to_solr(vec, cat_codes)
		stop = timeit.default_timer()
		print "Time to query solr=", stop - start

	print "Categories =", total_cats
	results = remove_dups(results)
	results = sorted(results, key=lambda x: x['score'], reverse=True)[:10]
	fig = plt.figure(figsize=(3, 10))
	ax = fig.add_subplot(6, 2, 1)
	plt.imshow(image_np[:, :, ::-1], label="score")
	plt.axis('off')
	ax.set_title("query image", fontsize=5)
	for result in results:
		img = read_image("../" + result['imageURL'])
		ax = fig.add_subplot(6, 2, results.index(result) + 2)
		plt.imshow(img[:, :, ::-1], label="score")
		plt.axis('off')
		ax.set_title("score=" + str(result['score']), fontsize=5)
		ax.set_aspect('equal')
	fig.tight_layout()


def search_by_url(path):
	start = timeit.default_timer()
	detected_objects = detect_object(path)
	stop = timeit.default_timer()
	if len(detected_objects) == 0:
		print "Cant detect any object, searching for whole image"
		detected_objects = [read_image(path)]
	print "Detected objects = " + str(len(detected_objects)) + ", Time to detect objects=" + str(stop - start)
	for object in detected_objects:
		print "Image Dimension =", object.shape
		search_by_image(object)
	plt.tight_layout()
	plt.show()


def remove_dups(results):
	results_tmp = []
	urls = set([])
	for result in results:
		if not result['imageURL'] in urls:
			urls.add(result['imageURL'])
		else:
			results_tmp.append(result)
	return results_tmp


def query_to_solr(vec, categories):
	print "Querying solr for categories =", categories
	categories = " OR ".join(set(categories))
	vector = ",".join(str(x) for x in vec)
	params = \
		'fl=categories,score,imageURL&' \
		'indent=on&' \
		'q={!vp f=vector vector="' + vector + '"}&fq=categories: (' + categories + ')&rows=20&wt=json'
	response = requests.post(url + '/select', headers={"Content-Type": "application/x-www-form-urlencoded"},
							 data=params)
	docs = response.json()['response']['docs']
	return [doc for doc in docs if doc['score'] > configs['SOLR_SCORE_THRESH']]


if __name__ == '__main__':
	start = timeit.default_timer()
	search_by_url('/Users/coviam/image_search/test/sample2.jpg')
	stop = timeit.default_timer()
	print "Time to load entire result =", stop - start
