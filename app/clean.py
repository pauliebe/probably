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

def find_nextwords(parsed_json, query):
    stop = define_stopwords(query)

    next_words = []
    missing_query_list = []
    for item in parsed_json:
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

#next_words, missing_query_list = find_nextwords(parsed_json,stop)

def find_phrases(parsed_json, query):
    next_phrases = []
    missing_query_list = []
    last_phrases = []
    
    for item in parsed_json:
        title = word_tokenize(item['title'].lower().strip(']').strip('[').strip('"'))
        try:
            query_index = title.index(query)
        except ValueError:
            missing_query_list.append(item['title'])
            continue
            
        if query_index == len(title)-1:
            last_phrase = title[:query_index]
            last_phrases.append(title)
        else:
            next_phrase = title[query_index:]
            next_phrases.append(next_phrase)
    
    return next_phrases, missing_query_list, last_phrases

def make_dict(filename, query):
    parsed_json = load_json(filename)
    next_words = find_nextwords(parsed_json, query)
    next_phrases, missing_query_list, last_phrases = find_phrases(parsed_json, query)

    categories = {}

    for item in next_words:
        categories[item] = []

    for item in next_phrases:
        test = item[1]
        if test in categories:
            title_list = categories[test] 
            #untokenize
            title_list.append("".join([" "+i if not i.startswith("'") and i not in string.punctuation else i for i in item]))
    
    return categories 
