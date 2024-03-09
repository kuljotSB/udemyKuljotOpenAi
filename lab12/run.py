import os
import json
import requests
import openai
import dotenv
from dotenv import load_dotenv

load_dotenv()
url=os.getenv("URL")
api_key=os.getenv("API_KEY")
cv_endpoint=os.getenv("CV_ENDPOINT")
cv_key=os.getenv("CV_KEY")

headers={
    "Content-Type":"application/json",
    "api-key": api_key

}

json_data = {
    "enhancements": {
            "ocr": {
              "enabled": True
            },
            "grounding": {
              "enabled": True
            }
    },
    "dataSources": [
    {
        "type": "AzureComputerVision",
        "parameters": {
            "endpoint": cv_endpoint,
            "key": cv_key
        }
    }],
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": [
	            {
	                "type": "text",
	                "text": "Describe this picture:"
	            },
	            {
	                "type": "image_url",
	                "image_url": {
                        "url":"https://learn.microsoft.com/azure/ai-services/computer-vision/media/quickstarts/presentation.png" 
                    }
                }
           ] 
        }
    ],
    "max_tokens": 100, 
    "stream": False 
}

response=requests.post(url,headers=headers,json=json_data).json()

def get_details():
    caption=response['choices'][0]['message']['content']
    print(caption)
    
get_details()
    
