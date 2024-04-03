import requests
import os
from dotenv import load_dotenv
import json
from openai import AzureOpenAI

load_dotenv()

key = os.getenv("KEY")
endpoint_url = os.getenv("ENDPOINT")
whisper_model=os.getenv("WHISPER_MODEL")
chat_model=os.getenv("CHAT_MODEL")

final_url = f"{endpoint_url}/openai/deployments/{whisper_model}/audio/transcriptions?api-version=2023-09-01-preview"

headers = {
    "api-key": key,
}

file_path = r".\voice.mp4"

# Open the file in binary mode and close it after reading
with open(file_path, "rb") as file:
    files = {
        "file": (os.path.basename(file_path), file, "application/octet-stream")
    }

    final_response = requests.post(final_url, headers=headers, files=files).json()
    
    user_prompt=final_response['text']

    client = AzureOpenAI(
  azure_endpoint = endpoint_url, 
  api_key=key,  
  api_version="2024-02-15-preview"
   )  

    response = client.chat.completions.create(
      model=chat_model,
      messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": user_prompt}
     ]
    )
    
    print(response.choices[0].message.content)








