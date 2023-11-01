#importing important utilities and libraries
import json
import requests
import openai
import os

#setting openai configuration details
openai.api_key = os.getenv('get_oai_key')
openai.api_base = os.getenv('get_oai_base')
openai.api_version = "2023-03-15-preview"
deployment_name = "Your deployment name here"
openai.api_type = "azure"

api_url = "your_api_url_here"

data="a lot of festivals are coming"

input_data = {
    "input":data
}

#setting the api_key for the POST method of the reponse library
api_key_header = {
    "api-key":openai.api_key
}

get_data = requests.post(api_url, data=input_data, headers = api_key_header)

#retrieving the JSON object 
get_output = get_data.json()

#printing the output
print(get_output['data'][0]['embedding'])



