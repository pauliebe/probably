import requests

def make_preposition_list(location): #adds various prepositions to the query
	prepositions = ['in', 'at', 'around', 'on', 'by', 'above', 'along']
	preposition_list = []
	preposition_list.append(location)

	for preposition in prepositions:
		new_query = '{preposition} {query}'.format(preposition=preposition, query=location)
		preposition_list.append(new_query)

	return preposition_list

def make_modifier_list(location): #adds modifer 
	modifiers = ['likely', 'maybe', 'probably']
	preposition_list = make_preposition_list(location)
	modifier_list =[]

	for modifier in modifiers:
		for preposition in preposition_list:
			new_query = '%s %s' %(modifier, preposition)
			modifier_list.append(new_query)

	return modifier_list

def search_LOC(preposition_list):

	for item in preposition_list: #loop through preposition list to cover variety of phrasing
		url = 'https://www.loc.gov/pictures/search/?q=' + item + '&fo=json'
		print (url)

		loc_response = requests.get(url)

		print(loc_response)
		loc_response.raise_for_status() #check response status
		query_response_json = loc_response.json() #get JSON

		while True:
			#loop through results to find titles with query word in it
			for response in query_response_json['results']:
				if item in response['title']:
					print(response['title'])

			next_page = query_response_json['pages']['next']

			if next_page is not None: #go on to next page of responses
				query_response_json = requests.get('https:' + next_page + '&fo=json').json()

			else:
				break

# program starts
print ('Where do you want to search?')
location = input()
modifier_list = make_modifier_list(location)

search_LOC(modifier_list)



'''

make flask




lists to sort through:
preposition
modifier


location


to store:

location
title
creator
image['full']


rights (where???)


Possible probably prepositions:
probably in
probably at
probably around
probably about
probably above
probably along
probably below
probably besides
probably by
probably into
proably near
probably off
probably on
probably opposite
probably outside
probably over
proably within
probably located


for 
'''