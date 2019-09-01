init:
	pip install -r requirements.txt
	python -m nltk.downloader stopwords punkt

search:
	python searching/search.py

find_images: 
	python searching/images.py

write_data:
	python cleaning/write_data.py