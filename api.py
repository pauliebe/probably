import requests

def findProbably(query):
	loc_request = requests.get('https://www.loc.gov/pictures/search/?q='+ query + '&fo=json')
	loc_request.raise_for_status() #check response status
	query_response_json = loc_request.json()#get JSON

	while True:
		#loop through results to find titles with query word in it
		for response in query_response_json['results']:
			next_page = answers_json['pages']['next']
			print(next_page) #test to see what's going on 

			if query in response['title']:
				print(response['title'])

		if next_page is not None: #go on to next page of responses
			query_response_json = requests.get('https:' + next_page + '&fo=json').json()

		else:
			break
		

print ('Where do you want to search?')
user_query = raw_input()

findProbably(user_query)



'''
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