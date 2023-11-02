#importing important utilities and libraries
import openai
import requests
import os
import json

#setting important configurations
openai.api_key = os.getenv('oai_key')
openai.api_base=os.getenv('oai_base')

#sending a GET method to our indexer to get outputs
url =""
response=requests.get()

#creating a json object
output=response.json()

#using ChatCompletion function
data=output....#modify this by seeing the api documentation

finalResponse=openai.ChatCompletion.create(
    engine="YOUR_ENGINE_HERE",
    temperature=0.7,
    messages=[
        {"role":"system", "content":"you are an assistant that helps the user to summarise the article content"},
        {"role":"user", "content":data}
    ]
)

print(finalResponse.choices[0].message.content + "\n")



