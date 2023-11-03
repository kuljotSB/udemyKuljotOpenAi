#importing important utilities and libraries
import os
import requests
import json
import openai
from dotenv import load_dotenv

#setting configurations
load_dotenv()
openai.api_key=os.getenv('oai_key')
openai.api_base=os.getenv('oai_base')

def getWeather(location):
    #first getting the latitude and longitude for the particular location
    url="http://api.openweathermap.org/geo/1.0/direct?q=location&limit=1&appid=e27ba001ff084034c56e8a7e7281820b"
    first_response=requests.get(url)
    latitude=first_response.content.lat
    longitude = first_response.content.lon

    #sending another API call to get the weather conditions in a real-time case scenario
    url_final="https://api.openweathermap.org/data/2.5/weather?lat=latitude&lon=longitude&appid=e27ba001ff084034c56e8a7e7281820b"
    final_response=requests.get(url_final)
    final_message=final_response.content.weather[0].description
    print("the weather condition is:" , " " , final_message)
    
def run_conversation(messages, functions, available_functions, deployment_id):
    response=openai.ChatCompletion.create(
        deployment_id=deployment_id,
        messages=messages,
        functions=functions,
        function_call="auto",
        temperature=0.2
    )
    response_message=response["choices"][0]["message"]

    #call the function
    function_name=response_message["function_call"]["name"]

    #verify if the function exists
    if function_name not in available_functions:
        return "Function" + function_name + "does not exist"
    function_to_call=available_functions[function_name]

    function_args = json.loads(response_message["function_call"]["arguments"])
    function_response = function_to_call(function_args)

    print(function_response)
    print()


def main():
    
    
    functions=[
        {
            "name":"getWeather",
            "description":"Retrieve documents from the azure cognitive search index",
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

    available_functions={"getWeather":getWeather}
    messages=[
    {"role":"system", "content":"you are an assistant that retrieves real-time weather of a particular location"},
    {"role":"user", "content":"how is the weather in Mumbai, India"}
]
    deployment_id="prabhjotturbofm"

    run_conversation(messages=messages, functions=functions, available_functions=available_functions, deployment_id=deployment_id)

if __name__=="__main__":
    main()
    










                     
