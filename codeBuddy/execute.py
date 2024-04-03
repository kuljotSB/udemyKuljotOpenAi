#importing important libraries and utilities
import openai
import os
import json
import requests
from openai import AzureOpenAI

#setting important configurations and credentials
azure_key = "YOUR_AZURE_OAI_KEY_HERE"
azure_endpoint="YOUR_AZURE_OAI_ENDPOINT_HERE"
model_name="YOUR_MODEL_NAME_HERE"

def response(oai_key, oai_endpoint, user_input):
    #creating an Azure Open AI client
    client = AzureOpenAI(
        azure_endpoint=azure_endpoint,
        api_key = azure_key,
        api_version="2024-02-15-preview"
    )
    #creating the "messages" part of the chat completions API
    messages=[
        {"role":"system", "content":"you are an AI assistant"},
        {"role":"user", "content":prompt}
    ]
    #calling the chat completions API to retrieve response from our chat engine
    final_response = client.chat.completions.create(
        model=model_name,
        messages=messages,
        temperature=0.7
    )
    #printing the final response content
    print(final_response.choices[0].message.content)
    
#writing functional code for performing the correct set of operations
num = input("enter 1 to debug code and 2 for unit tests to your code")

if(num=='1'):
    file = open(file=r'.\factorial.py', encoding='utf8').read() #change the file path according to your user directory
    prompt="please debug this code in python \n" + file
    response(azure_key,azure_endpoint,prompt)
    
else:
    file=open(file=r'.\function.py', encoding='utf8').read() #change the file path according to your user directory
    prompt="please provide unit tests for the following code in python \n" + file
    response(azure_key,azure_endpoint,prompt)
    
