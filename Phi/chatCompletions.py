import urllib.request
import json
import os
import asyncio
import ssl
from dotenv import load_dotenv
import requests
# Request data goes here
# The example below assumes JSON formatting which may be updated
# depending on the format your endpoint expects.
# More information can be found here:
# https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
data =  {
  "messages": [
    {
      "role": "user",
      "content": "I am going to start a new job, what should I look out for?"
    }
  ],
  "max_tokens": 1024,
  "temperature": 0.7,
  "top_p": 1
}

body = str.encode(json.dumps(data))

load_dotenv()
url = os.getenv("URL")
# Replace this with the primary/secondary key, AMLToken, or Microsoft Entra ID token for the endpoint
api_key = os.getenv("API_KEY")
if not api_key:
    raise Exception("A key should be provided to invoke the endpoint")


print("GENERATING ANSWER...")

headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
result =  requests.post(url=url, headers=headers, data=body)
json_result = result.json()
os.system('clear')
print(json_result['choices'][0]['message']['content'])


  
  


