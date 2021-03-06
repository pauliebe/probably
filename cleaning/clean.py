import json
import os
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.corpus import stopwords
import operator
from collections import Counter
import string
import re

detokenizer = TreebankWordDetokenizer()

#This script tokenizes title words
#figures out the word right after the query in those titles
#creates a dictionary sorted by those "next_words"
#for each title, matches an image from the LOC, a url from the LOC and the LOC pk number

#define stopwords
def define_stopwords(query):
    punctuation = list(string.punctuation)
    digits = list(string.digits)
    extra = [query, '\'s', '\'\'', '``', '--', '...', 'n\'t', '\'d', '\'ll', '\'re', '\'m']
    prepositions = ['in', 'at', 'on']
    stop = stopwords.words('english') + punctuation + digits + extra
    new_stopwords = [ w for w in stop if w not in prepositions]

    return new_stopwords

def load_json(filename):
    with open(filename) as json_data:
        #load json file
        parsed_json = json.load(json_data)

        return parsed_json

#WORD COUNT FUNCTIONS
def count_total(data):
    return len(data)

def count_common(query, data, count):
    
    stop = define_stopwords(query)
    count_all = Counter()

    for item in data:
        title = word_tokenize(item['title'].lower())
        #create list with all terms minus stop
        terms_stop = [term for term in title if term not in stop]
        count_all.update(terms_stop)

        count_list = count_all.most_common(count)

    return count_list

#determines words right after the query
def find_nextwords(data, query):
    stop = define_stopwords(query)
    next_words = []
    missing_query_list = []
    for item in data:
        title = word_tokenize(item['title'].lower().strip(']').strip('['))
        try:
            query_index = title.index(query)
        except ValueError:
            missing_query_list.append(item['title'])
            continue
        try:
            next_word = title[query_index+1]
        except IndexError:
            next_word = 'last_word'
            continue
        if next_word not in stop:
            next_words.append(next_word)

    return next_words

#splits titles right after query or right before, if it's the last word in the title
def find_phrases(data, query):
    next_phrases = {}
    missing_query_list = []
    last_phrases = {}
    
    for item in data:
        title = word_tokenize(item['title'].lower().strip(']').strip('[').strip('"'))
        try:
            query_index = title.index(query)
        
        except ValueError:
            missing_query_list.append(item['title'])
            continue
            
        if query_index == len(title)-1:
            last_phrase = title[:query_index]
            last_phrases[item['pk']] = last_phrase
        else:
            if title[query_index-1] == '(':
                next_phrase = title[(query_index-1):]
            else:
                next_phrase = title[query_index:]
            next_phrases[item['pk']] = next_phrase

    
    return next_phrases, missing_query_list, last_phrases

#clean pk
def clean_pk(pk):
	if '/' in pk:
		cleaned = pk.replace('/', '_')	
		return cleaned
	else:
		return pk

#match images
def make_img_path(pk, base_path):
    cleaned_pk = clean_pk(pk)
    img_path = '%s/static/img/%s.jpg' %(base_path, pk)
    rel_img_path = 'static/img/%s.jpg' %(cleaned_pk)
    return img_path, rel_img_path


#builds a dictionary that matches split titles to imgs and url

def make_dict(data, query, base_path):
    print('Finding ' + query +' in ' + str(len(data)) + ' records')

    next_words = find_nextwords(data, query)
    next_phrases, missing_query_list, last_phrases = find_phrases(data, query)
    details= {}
    categories = {}

    for next_word in next_words:
        categories[next_word] = {}
    
    print ('Matching images and putting everything back together')

    for item in data:
        pk =item['pk']
        img_path, rel_img_path = make_img_path(pk, base_path)
        details[pk] ={
            'pk': pk,
            'url': item['links']['item'],
            'title': item['title'],
            'subjects': item['subjects']
        }

        if os.path.exists(img_path):
            details[pk]['img'] = rel_img_path
        else:
            pass
    
        for item in next_phrases:
            tokens = next_phrases[item]
            clean_title = detokenizer.detokenize(tokens)
            short_title = sent_tokenize(clean_title)
            if item == pk:
                details[pk]['title_snippet'] = short_title[0]
                
    print ('Done!')

    return details
