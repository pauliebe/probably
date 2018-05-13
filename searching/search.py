import requests
import json
import os

#This script takes in a query
#searches the Library of Congress pictures collection for that query 
#Stores JSON data for each result as query_pk (pk is an LOC identifier )into a folder called "query"
#Combines all the results into a JSON file called query.json, into a folder called "combined"

query = input('What\'s your query?')
json_directory = os.path.abspath('json_archive/%s' %(query))
combined_json_path = os.path.abspath('../app/json_files/%s.json' %(query))

#search LOC API
def search_LOC(query):
		url = 'http://www.loc.gov/pictures/search/?q=%22'+ query + '%22&fi=title&fo=json' 
		loc_response = requests.get(url)

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

	filename = '%s_response_%s.json' %(query, pk)

	if not os.path.exists(json_directory):
		os.makedirs(json_directory) #make new directory if it's a new search

	if not os.path.exists('%s/%s' %(json_directory, filename)): #check if file exists
		with open('%s/%s' %(json_directory, filename), 'w') as outfile:
			json.dump(result, outfile, sort_keys=True, indent=4)

	else:
		print('That search has been completed, according to all the files in the %s folder' %(query))

#combine into files in input_directory to a single file (output_filename)
def combine_json(input_directory, output_filename):
	result = []

	for filename in os.listdir(input_directory):
		with open('%s/%s' %(input_directory, filename)) as infile:
			if not filename == '.DS_Store': #This is weird
				print(filename)
				result.append(json.load(infile))

	with open(output_filename, 'w') as outfile:
		json.dump(result, outfile, sort_keys=True, indent=4)

#execute search
if os.path.exists(json_directory):
	print('This search has been completed')
	if os.path.exists(combined_json_path):
		print('And this the json has been combined')
	else:
		combine_json(json_directory, combined_json_path)

else:
	os.makedirs(json_directory) #make new directory if it's a new search
	search_LOC(query)
	combine_json(json_directory, combined_json_path)

