from embedding import get_embedding, read_image
from solr_indexer import update_to_solr, index_all
from configs import configs

IMAGE_URL = "../test/heels1.jpg"


def test_embedding():
	image_np = read_image(IMAGE_URL)
	embedding = get_embedding(image_np)
	print "Vector Representation=", embedding.shape


def test_configs():
	print configs


def test_upload_solr():
	image_np = read_image(IMAGE_URL)
	embedding = get_embedding(image_np)
	update_to_solr(embedding, IMAGE_URL, ['test'])


def test_index_all():
	index_all()

if __name__ == '__main__':
	# index_all()
	# test_upload_solr()
	# test_configs()
	test_embedding()
