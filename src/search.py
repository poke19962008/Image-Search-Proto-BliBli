from embedding import get_embedding, read_image
from category_classifier import get_intent_categories
from configs import configs
from matplotlib import pyplot as plt
import cv2 as cv
import requests

HOST = configs['SOLR_HOST']
COLL = configs['SOLR_COLL']
url = 'http://' + HOST + '/solr/' + COLL


def search_by_url(path):
	image_np = read_image(path)
	print "Image Dimension =", image_np.shape
	flip_horizontal = cv.flip(image_np, 1)
	aug_images = [image_np, flip_horizontal]

	results = []
	total_cats = []
	for images in aug_images:
		vec = get_embedding(images)
		cats = get_intent_categories(images)
		total_cats += cats
		cat_codes = [cat[0] for cat in cats]
		results += query_to_solr(vec, cat_codes)

	print "Categories =", total_cats
	results = remove_dups(results)
	results = sorted(results, key=lambda x: x['score'], reverse=True)[:10]
	fig = plt.figure(figsize=(8, 8))
	fig.suptitle('BliBli', fontsize=15)
	for result in results:
		img = read_image("../" + result['imageURL'])
		ax = fig.add_subplot(5, 2, results.index(result)+1)
		plt.imshow(img[:, :, ::-1], label="score")
		plt.axis('off')
		ax.set_title("Score=" + str(result['score']), fontsize=5)
	fig.tight_layout()
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
	search_by_url('/Users/coviam/obj_test/000148.jpg')
