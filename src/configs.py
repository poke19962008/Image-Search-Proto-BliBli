configs = {
	'K': 10,
	'POS_THETA': .8,
	'FILE_RANGE': 37000,
	'PRECISION': 2,
	'SOLR_SCORE_THRESH': -1,
	'CATEGORY_THRESH': 10,
	'TOP_CATEGORIES_DETECTED': 2,
	'debug': True,
	'CAT_CLASS': {
		'batch': 2000,
		'category_thresh': 10,
		'cat_lower_limit': 1,
		'cat_upper_limit': 3,
		'epochs': 10
	},
	'SOLR_HOST': 'x-search-solr-1.qa1-sg.cld:8983',
	'SOLR_COLL': 'imageSearch',
	'EMBEDDING_MODEL': '../models/embedding/1'
}
