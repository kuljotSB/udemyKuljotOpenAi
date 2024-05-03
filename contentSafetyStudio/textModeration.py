import json
import requests
import openai
from openai import AzureOpenAI
import os
import dotenv
from dotenv import load_dotenv

load_dotenv()

text = input("input query for the GPT engine")

content_safety_base = os.getenv("CONTENT_SAFETY_BASE")

url = os.getenv("CONTENT_SAFETY_BASE")+"contentsafety/text:analyze?api-version=2023-10-01"


headers = {
    "Ocp-Apim-Subscription-Key": os.getenv("CONTENT_SAFETY_KEY") ,
    "Content-Type": "application/json"

}
body = {
    "text":text
    
}

response = requests.post(url,headers=headers,json=body)

json_response = response.json()


hateResult = json_response['categoriesAnalysis'][0]['severity']
selfHarmResult = json_response['categoriesAnalysis'][1]['severity']
sexualResult = json_response['categoriesAnalysis'][2]['severity']
violenceResult = json_response['categoriesAnalysis'][3]['severity']

#setting the threshold value
threshold = 2


if hateResult > threshold:
    print("Hate speech detected")
elif selfHarmResult > threshold:
    print("Self harm detected")
elif sexualResult > threshold:
    print("Sexual content detected")
elif violenceResult > threshold:   
    print("Violence detected")
else:
    
    client = AzureOpenAI(
        azure_endpoint = os.getenv("OPENAI_API_BASE"),
        api_key=os.getenv("OPENAI_API_KEY"),
        api_version="2024-02-15-preview"
        
    )
    
    messages = [
        {
            "role":"system",
            "content":"You are a helpful assistant that will help answer user queries"
        },
        {
            "role":"user",
            "content":text
        }
    ]
    
    response = client.chat.completions.create(
        model = os.getenv("OPENAI_CHAT_MODEL"),
        messages=messages,
        temperature=0.7,
    )
    
    print(response.choices[0].message.content + "\n")
    

        
        


