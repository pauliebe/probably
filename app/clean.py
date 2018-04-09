import json
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import operator
from collections import Counter
import string

#This script tokenizes title words
#creates a new dictionary
#key is pk_number, value is title: ['list', 'of', 'title', 'words']
#and then tell you the most frequent words after the query word in the titles

query = input('Query?')
json_path = 'json_files/combined/%s.json' %(query)
titles = {}

#define stopwords
punctuation = list(string.punctuation)
digits = list(string.digits)
extra = list(query + '\'s')
stop = stopwords.words('english') + punctuation + digits + extra

def add_to_dict(filename):
	with open(filename) as json_data:
		#load json file
		parsed_json = json.load(json_data)

		count_all = Counter()
		#add items to dictionary
		for item in parsed_json:
			title = word_tokenize(item['title'].lower()) #add tokenized title to dict

			#create list with all terms minus stop
			terms_stop = [term for term in title if term not in stop]
			count_all.update(terms_stop)

			print(count_all.most_common(15))
	

add_to_dict(json_path)
#count_words(titles)

