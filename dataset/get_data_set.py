import requests, json, urllib, sys

ROWS = 1000
PREFIX = 'https://www.static-src.com/wcsstore/Indraprastha/images/catalog/medium/'


def get_document(start):
	cookies = {
		'JSESSIONID': 'F013510061BD3C24361AF552A45C969B',
		'_ga': 'GA1.2.321933754.1539761137',
		'cto_lwid': '2e806c9d-c8b9-4b00-8aba-ab62dafe5ee2',
		'__bwa_user_id': '1916329177.U.4066437063030459.1539867082',
		'__bwa_user_session_sequence': '296',
		'__ssid': '78c06f178bc67d727082ef8c58a1c1b',
		'_fbp': 'fb.1.1567504356618.231977081',
		'cto_bundle': 'M7wKt18yZ0VRTSUyRnY3ZUJoUEtHVFBTdW9pOGI2cWJaNEgwNnFRbzZsVnBuUVc2SnBaeENETFJlTzhweTl0cVNOU0IyRW9URFlYSmJQMkladnh6OUVjYU4lMkZUMXYxd0ZtN0pnNzR1djMlMkY1Y2JvNnNoR2FobGJuMDN4WXZSbDZVd250dEduQXlEOHglMkJCSHBzaDZLU3JkMWZNRWolMkJwV1hicyUyRmRBNTVCOGxxV1FJNWRLbDglM0Q',
		'INGRESSCOOKIE': '165611d77ff73f76facdf603846d05d7',
	}

	headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:70.0) Gecko/20100101 Firefox/70.0',
		'Accept': 'application/json, text/plain, */*',
		'Accept-Language': 'en-US,en;q=0.5',
		'Content-Type': 'application/json;charset=utf-8',
		'Origin': 'https://searchcenter.gdn-app.com',
		'Connection': 'keep-alive',
		'Referer': 'https://searchcenter.gdn-app.com/x-search/view/solr-query',
		'x-forwarded-for': 'blibli.com',
		'Cache-Control': 'max-age=0',
	}

	params = (
		('collectionName', 'productCollectionAlias'),
		('query', 'fl=mediumImage,salesCatalogCategoryIds&fq=salesCatalogCategoryIds:54912&indent=on&q=*:*&rows=' + str(
			ROWS) + '&wt=json' + '&start=' + str(start)),
		('requestHandler', 'select'),
	)

	data = {
		'{"collectionName":"productCollectionAlias","requestHandler":"select","query":"fl': 'sku,name,mediumImage',
		'fq': 'salesCatalogCategoryIds:54912',
		'indent': 'on',
		'q': '*:*',
		'rows': '100',
		'wt': 'json"}'
	}

	response = requests.post('https://searchcenter.gdn-app.com/x-search/api/solr-query-data', headers=headers,
							 params=params, cookies=cookies, data=data)
	print response.text
	return json.loads(response.json()['errorMessage'])['response']['docs']


if __name__ == '__main__':
	fileName = 'dataset.txt'
	if len(sys.argv) > 1:
		fileName = sys.argv[1]
	start = 0
	while True:
		try:
			images = get_document(start)
			if len(images) == 0:
				break
			print 'Start=', start
			for image in images:
				image_url = image['mediumImage']
				local_image_url = 'dump/' + image_url.split('/')[-1]
				urllib.urlretrieve(PREFIX + image_url, local_image_url)
				with open(fileName, 'a') as f:
					data = {'dir': local_image_url, 'label': image['salesCatalogCategoryIds']}
					f.write(json.dumps(data) + '\n')
			start += ROWS
		except Exception as e:
			print e
			start += ROWS
			continue
