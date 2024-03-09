import json
import requests
import openai
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

#creating an Azure OpenAI client
load_dotenv()
client = AzureOpenAI(
  azure_endpoint = os.getenv("oai_base"), 
  api_key=os.getenv("oai_key"),  
  api_version="2023-05-15"
)


functions=[
        {
            "name":"getWeather",
            "description":"Retrieve real-time weather information/data about a particular location/place",
            "parameters":{
                "type":"object",
                "properties":{
                    "location":{
                        "type":"string",
                        "description":"the exact location whose real-time weather is to be determined",
                    },
                    
                },
                "required":["location"]
            },
        }
    ] 

messages=[
    {"role":"system", "content":"you are an assistant that helps people retrieve real-time weather data/info"},
    {"role":"user", "content":"how is the weather in Mumbai?"}
    
]

initial_response = client.chat.completions.create(
    model="YOUR_MODEL_NAME", # model = "deployment_name".
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "How is the weather in Mumbai?"}
    ],
   functions=functions
)


function_name = initial_response.choices[0].message.function_call.name
function_argument = json.loads(initial_response.choices[0].message.function_call.arguments)
location= function_argument['location']
print(location)
#calling open weather map API for information retrieval
#fetching latitude and longitude of the specific location respectively
url = "http://api.openweathermap.org/geo/1.0/direct?q=" + location + "&limit=1&appid=55c620986802c3a6d0fbb8f81733728d"
response=requests.get(url)
get_response=response.json()
latitude=get_response[0]['lat']
longitude = get_response[0]['lon']

url_final = "https://api.openweathermap.org/data/2.5/weather?lat=" + str(latitude) + "&lon=" + str(longitude) + "&appid=55c620986802c3a6d0fbb8f81733728d"
final_response = requests.get(url_final)
final_response_json = final_response.json()
weather=final_response_json['weather'][0]['description']
print(weather)

