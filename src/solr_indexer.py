import requests, json
from configs import configs
from threading import Thread
from util import get_embedding, read_image

HOST = configs['SOLR_HOST']
COLL = configs['SOLR_COLL']
# HOST = "xsearch-solr7-02.perf.lokal:8983"
# COLL = "imageSearch_flatten"


url = 'http://' + HOST + '/solr/' + COLL
headers = {
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0',
	'Accept': 'application/json, text/plain, */*, application/x-www-form-urlencoded',
	'Accept-Language': 'en-US,en;q=0.5',
	'Content-type': 'application/json',
	'Connection': 'keep-alive',
	'Referer': 'http://seoulsolr6-01.dev1.lokal:8983/solr/',
	'x-forwarded-for': 'blibli.com',
}


def convert_to_solr_vec(vec):
	return " ".join([str(x) + "|" + str(y) for x, y in zip(range(0, len(vec)), vec)])


def update_to_solr(vec, image_link, category, ind):
	params = (
		('_', '1570789966606'),
		('boost', '1.0'),
		('commitWithin', '1000'),
		('overwrite', 'true'),
		('wt', 'json'),
	)
	data = '[{"imageURL":"' + image_link + '", "vector":"' + convert_to_solr_vec(vec) + \
		   ' ", "categories": ' + json.dumps(category) + '}]'
	response = requests.post(url + '/update', headers=headers, params=params, data=data)
	print response.json(), image_link.split('/')[-1], ind


def query_to_solr(vec, categories):
	params = \
		'fl=categories,score,imageURL&' \
		'indent=on&' \
		'q={!vp f=vector vector="' + ",".join(str(x) for x in vec.eval()) + '"}&' \
																			'fq=categories: (' + " OR ".join(
			categories) + ')&' \
						  'rows=5&' \
						  'wt=json'
	response = requests.post(url + '/select', headers={"Content-Type": "application/x-www-form-urlencoded"},
							 data=params)
	docs = response.json()['response']['docs']
	return [doc for doc in docs if doc['score'] > configs['SOLR_SCORE_THRESH']]


def index_all(source="dataset/"):
	images, categories = [], []
	with open('../dataset/dataset.txt') as f:
		raw_file = f.readlines()[:configs['FILE_RANGE']]
		raw_file = set(raw_file)
	for record in raw_file:
		data = json.loads(record)
		link = 'dataset/' + data['dir']
		images.append(link), categories.append(data['label'])

	print "Images=", len(images), "Categories=", len(categories)
	for image_, cat in zip(images, categories):
		try:
			image_np = read_image("../"+image_).squeeze()
			vec = get_embedding(image_np)
			ind = images.index(image_)
			t = Thread(target=update_to_solr, args=(vec, image_, cat, ind))
			t.start()
		except KeyboardInterrupt:
			raise
		except:
			continue
