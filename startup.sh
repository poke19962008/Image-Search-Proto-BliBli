source pyenv/
# startup embedding tf serving
# To save embedding models -> python2 embedding.py
nohup tensorflow_model_server --model_base_path=/data/image-search-blibli/models/embedding/ --rest_api_port=9000 --model_name=embedding > /data/image-search-blibli/logs/tf-serving-embedding.log&
