configs = {
	'K': 10,
	'POS_THETA': .8,
	'FILE_RANGE': 37000,
	'PRECISION': 2,
	'SOLR_SCORE_THRESH': -1,


	'debug': True,
	'CAT_CLASS': {
		'batch': 2000,
		'category_thresh_bucket': 100,
		'cat_lower_limit': 1,
		'cat_upper_limit': 3,
		'epochs': 10,
		'CATEGORY_THRESH': 10,
		'TOP_CATEGORIES_DETECTED': 2,
		'model_path': '../models/category/1'
	},
	'EMBEDDING_TFX_HOST': 'http://image-search-ml.qa1-sg.cld:8983',
	'CAT_CLASSIFIER_TFX_HOST': 'http://image-search-ml.qa1-sg.cld:8983',
	'SOLR_HOST': 'x-search-solr-1.qa1-sg.cld:8983',
	'SOLR_COLL': 'imageSearch',
	'EMBEDDING_MODEL': '../models/embedding/1',
	'TFX': False
}
