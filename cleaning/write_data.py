from clean import make_dict, load_json
import json
import os

temp_dict = {}

def write_json(output_path, data):
    with open(output_path, 'w') as file:
     file.write(json.dumps(data))

def write_data(query):
    base_path= os.path.abspath('../app/')
    input_path = os.path.abspath('../app/static/json_files/%s.json' %(query)) 
    data = load_json(input_path)
    details= make_dict(data,query, base_path)
    output_path = os.path.abspath('../app/static/json_files/%s-details.json' %(query))
    write_json(output_path, details)

query = input('Write data for what?')
write_data(query)