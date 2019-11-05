alias reindex="cd /data/image-search-blibli/src;nohup python2 -u solr_indexer.py &> ../logs/indexing.logs&"
alias reindex-logs="tail -f /data/image-search-blibli/logs/indexing.logs"

alias train-category="cd /data/image-search-blibli/src;nohup python2 -u category_classifier.py &> ../logs/cat_train.logs&"
alias train-category-logs="tail -f /data/image-search-blibli/logs/cat_train.logs"
# startup embedding tf serving
# To save embedding models -> python2 embedding.py
nohup tensorflow_model_server --model_base_path=/data/image-search-blibli/models/embedding/ --rest_api_port=8983 --model_name=embedding > /data/image-search-blibli/logs/tf-serving-embedding.log&
