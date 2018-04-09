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

#query = input('Query?')

titles = {}

#define stopwords
def define_stopwords(query):
	punctuation = list(string.punctuation)
	digits = list(string.digits)
	extra = [query, '\'s', '\'\'', '``', '--', '...', 'n\'t', '\'d', '\'ll', '\'re', '\'m']
	stop = stopwords.words('english') + punctuation + digits + extra

	return stop

def load_json(filename):
	with open(filename) as json_data:
		#load json file
		parsed_json = json.load(json_data)

		return parsed_json

def count_total(filename):
	return len(load_json(filename))

def count_common(query, filename, count):
	#filename = 'json_files/combined/%s.json' %(query)
	stop = define_stopwords(query)

	parsed_json = load_json(filename)

	count_all = Counter()
	#add items to dictionary
	for item in parsed_json:
		title = word_tokenize(item['title'].lower())
		#create list with all terms minus stop
		terms_stop = [term for term in title if term not in stop]
		count_all.update(terms_stop)

		count_list = count_all.most_common(count)

	return count_list
	


