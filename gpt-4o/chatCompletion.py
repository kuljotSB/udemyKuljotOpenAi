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

async def chat_completion():
    choice=""
    while(choice!="exit"):
        user_query = input("Enter your query: ")
        print("Processing...")
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_CHAT_COMPLETION_MODEL"),
            messages=[
                {
                    "role":"system",
                    "content":"you are a helpful ai assistant"
                },
                {
                    "role":"user",
                    "content":user_query
                }
            ],
            temperature=0.7
        )
        os.system('cls')
        print(response.choices[0].message.content)
        choice = input("type exit to exit or anything else to continue: ")
        
asyncio.run(chat_completion())


