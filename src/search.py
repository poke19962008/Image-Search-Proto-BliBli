from embedding import get_embedding, read_image


def search_by_url(path):
	image_np = read_image(path)
	vec = get_embedding(image_np)


if __name__ == '__main__':
	search_by_url('/Users/coviam/obj_test/000013.jpg')
