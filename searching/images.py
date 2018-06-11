import requests
import os
import json
import urllib.request
import re

#This script finds  the response urls
#and goes through every single one
#to determine if it's usable
#downloads if it is

def load_json(filename):
	with open(filename) as infile:
		data = json.load(infile)
	return data

def check_img_rights(rights):
	try:
		if 'public domain' in rights.lower():
			return True
		if 'no known restriction' in rights.lower():
			return True
		if 'no known copyright restriction' in rights.lower():
			return True  
		if 'no copyright restriction' in rights.lower():
			return True
		else:
			return False

	except KeyError:
		return 'KeyError'

def get_rights(data):
	try:
		if data['links']['resource'] is not None:
			resource_url = 'https:%s?fo=json' %(data['links']['resource'])
			response = requests.get(resource_url).json()
			try:
				rights = response['item']['rights_information']
			except KeyError:
				rights = 'KeyError'
					
		elif data['links']['item'] is not None: 
			resource_url = 'https:%s?fo=json' %(data['links']['item'])
			response = requests.get(resource_url).json()
			try:
				rights = response['item']['rights_information']
			except KeyError:
				rights = 'KeyError'

		else:
			rights = 'missing resource url'

	except ValueError:	
		rights = 'ValueError'
	
	return rights

def make_log(rights, pk, downloaded, output_path):

	if rights == 'missing resource url':
		log.write('PK: %s: There was no resource url. \n\n' %(pk))
		errors_dict[pk] = 'missing_resource_url'

	elif rights == 'ValueError':
		log.write('PK: %s. Maybe a group or something. Value error. \n\n' %(pk))
		errors_dict[pk]='ValueError'
	
	elif rights == 'KeyError':
		log.write('PK: %s. KeyError. \n\n' %(pk))

	else:
		log.write('PK: (%s)\n Rights: %s.\n' %(pk, rights))
		
		if downloaded == 'success' or downloaded == 'existing':
			log.write('Image downloaded: %s' %(output_path))
		
		elif downloaded == 'missing full img url':
			log.write('Image not downloaded: Full image url does not exist.\n\n')
			errors_dict[pk]='missing_full_img_url'
		
		elif downloaded == 'KeyError':
			log.write('Image not downloaded: KeyEror, maybe a group.\n\n')
			errors_dict[pk] = 'KeyError'
		elif downloaded == 'bad rights':	
			log.write('Image not downloaded: Bad rights.\n\n')

def download_img(img_url, output_path):
	opener = urllib.request.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	urllib.request.install_opener(opener)
	urllib.request.urlretrieve(img_url, output_path)

def clean_pk(pk):
	if '/' in pk:
		cleaned = pk.replace('/', '_')	
		return cleaned
	else:
		return pk

'''
SET VARIABLES
'''
query = input('Which query?')
base_path = os.path.abspath("../app/static/img/")
input_directory = os.path.abspath("json_archive/%s" %(query))
log_path = 'log-%s.txt' %(query)
error_path = 'errors-%s.txt' %(query)
errors_dict = {}
errors_file = open(error_path, 'w')
log = open(log_path, 'w')

''' 
RUN FULL SEARCH, DOWNLOAD AND LOG 
'''

for filename in os.listdir(input_directory):
	with open('%s/%s' %(input_directory, filename)) as infile:
		if not filename == '.DS_Store': #This is weird
			data = json.load(infile)
			pk = data['pk']
			cleaned_pk = clean_pk(pk)
			output_path = "%s/%s.jpg"%(base_path, cleaned_pk)
				
			if not os.path.exists(output_path):
				rights = get_rights(data)

				if check_img_rights(rights) == True:
					if data['image']['full']:
						img_url = "https:%s" %(data['image']['full'])
						download_img(img_url, output_path)
						downloaded = 'success'
					else:
						downloaded = 'missing full img url'
						pass

				elif check_img_rights(rights) == 'KeyError':
					downloaded = 'KeyError'
				else:
					downloaded = 'bad rights' 
					pass
			else:
				downloaded = 'existing'
			
			make_log(rights, pk, downloaded, output_path)

errors_file.write(json.dumps(errors_dict))
