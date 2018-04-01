import json

#This script will (eventually) combine json files in combined directory 
#into one dictionary pk:['list', 'of', 'title', 'words']
#to be then analyzed

titles = {}

def add_to_title_dict(filename):
	with open(filename) as json_data:
		parsed_json = json.load(json_data)
		print(parsed_json)
		title = parsed_json['title']
		pk = parsed_json['pk']
		titles[pk] = title

	return titles

filename = input('filename?')

add_to_title_dict(filename)
print(titles)
