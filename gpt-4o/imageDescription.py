import os
import requests
from openai import AzureOpenAI
import sys
import asyncio
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_KEY"),
  api_version="2024-02-15-preview"
)

async def describe_image():
        url = input("Enter the URL of the image: ")
        print("Processing...")
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_CHAT_COMPLETION_MODEL"),
            messages=[
                {
                    "role":"user",
                    "content":[
                        {"type":"text", "text":"what's in this image?"},
                        {"type":"image_url",
                         "image_url": 
                            {
                             "url": url
                            }
                        }
                    ]
                }
            ]
        )
        os.system('cls')
        print(response.choices[0].message.content)
    
asyncio.run(describe_image())
        
        
