import requests
import json
import pprint
import os.path

#find all probablies and dump em in files

#define search url as anything with probably in the title
url = 'http://www.loc.gov/pictures/search/?q=%22probably%22&fi=title&fo=json'

#search LOC API
def search_LOC(url):
		loc_response = requests.get(url)
		print(loc_response)

		loc_response.raise_for_status() #check response status
		query_response_json = loc_response.json() #get JSON

		while True:
			#loop through results to find titles with query word in it
			results = query_response_json['results']
			
			for result in results:
				write_json(result)

			next_page = query_response_json['pages']['next']

			if next_page is not None: #go on to next page of responses
				query_response_json = requests.get('https:' + next_page + '&fo=json').json()

			
			else:
				break
			
#write seperate json for each result
def write_json(result):
	pk = result['pk']

	if '/' in pk:
		pk = pk.replace('/', '_')	

	file_name = 'probably_response_%s.json' %(pk)

	if os.path.exists(file_name)  == False: #check if file exists
		with open(file_name, 'w') as outfile:
			json.dump(result, outfile, sort_keys=True, indent=4)

search_LOC(url)





#write this a json
	#loop thru that to search each pk number and write each response to a seperate file as pk.json
	#os.exist
	#check if that file exists before u run


