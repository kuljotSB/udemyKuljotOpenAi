import os
from dotenv import load_dotenv
import requests

# Add Azure OpenAI package
import openai
from openai import AzureOpenAI


def main(): 
        
    try: 
    
        
        
        # Read text from file
        text = open(file=r".\text_file.txt", encoding="utf8").read()
        
        print("\nSending request for summary to Azure OpenAI endpoint...\n\n")
        
        # Add code to build request...
        client = AzureOpenAI(
            azure_endpoint="YOUR_AZURE_ENDPOINT_HERE",
            api_key="YOUR_AZURE_OPENAI_KEY_HERE",
            api_version="2024-02-15-preview"
        )
        
        messages = [
            {"role":"system", "content":"you are an assistant that helps summarise text"},
            {"role":"user", "content":"summarise this text \n" + text}
        ]
        
        response = client.chat.completions.create(
            model = "YOUR_MODEL_NAME_GOES_HERE",
            temperature=0.7,
            messages=messages
        )
        
        print(response.choices[0].message.content)
        

    except Exception as ex:
        print(ex)

if __name__ == '__main__': 
    main()
