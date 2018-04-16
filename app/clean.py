import json
import os
from nltk.tokenize import WhitespaceTokenizer, word_tokenize
from nltk.corpus import stopwords
from nltk import bigrams, collocations
import operator
from collections import Counter
import string

#This script tokenizes title words
#creates a new dictionary
#key is pk_number, value is title: ['list', 'of', 'title', 'words']
#and then tell you the most frequent words after the query word in the titles


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

#WORD COUNT FUNCTIONS
def count_total(filename):
	return len(load_json(filename))

def count_common(query, filename, count):
	
	stop = define_stopwords(query)

	parsed_json = load_json(filename)

	count_all = Counter()

	for item in parsed_json:
		title = word_tokenize(item['title'].lower())
		#create list with all terms minus stop
		terms_stop = [term for term in title if term not in stop]
		count_all.update(terms_stop)

		count_list = count_all.most_common(count)

	return count_list

def count_bigrams(query, filename):

	parsed_json = load_json(filename)

	count_all = Counter()
	
	for item in parsed_json:
		title = word_tokenize(item['title'].lower())
		terms_stop = [term for term in title if term]
		
		bigrams_list = list(bigrams(terms_stop))
		count_all.update(bigrams_list)
		bigrams_count_list = count_all.most_common(5)

	return bigrams_list

def after_query(query, filename):
	parsed_json = load_json(filename)
	stop = define_stopwords(query)
	count_all = Counter()
	next_words=[]
	
	for item in parsed_json:
		title = word_tokenize(item['title'].lower())
		try:
			query_index = title.index(query)
		except ValueError:
			#print(title)
			continue
		try:
			next_word = title[query_index+1]
		except IndexError:
			next_word = 'last_word'
			continue
		if next_word not in stop:
			next_words.append(next_word)
		count_all.update(next_words)

	after_query_list = count_all.most_common(15)
	print(after_query_list)

	return after_query_list
