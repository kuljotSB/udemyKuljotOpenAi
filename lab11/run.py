import os
import json
import requests
import openai
from dotenv import load_dotenv

load_dotenv()
url=os.getenv("URL")
api_key=os.getenv("API_KEY")


headers={
    "Content-Type":"application/json",
    "api-key": api_key
}

body={
    "messages": [
        {"role":"system", "content":"You are a helpful assistant."},
        {"role":"user","content":[{
            "type":"text",
            "text":"Describe this picture"
        },
                                  {
                                      "type":"image_url",
                                      "image_url":{
                                          "url":"https://learn.microsoft.com/azure/ai-services/computer-vision/media/quickstarts/presentation.png",
                                          "detail":"high"
                                      }
                                  }]}
    ]
}

response=requests.post(url,headers=headers,json=body).json()
print(response)

