#importing importing libraries
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

#creating an azure openAi client
load_dotenv()
client = AzureOpenAI(
  azure_endpoint = os.getenv("OPENAI_API_BASE"), 
  api_key=os.getenv("OPENAI_API_KEY"),  
  api_version="2024-02-15-preview"
)

#send request to Azure OpenAi model
response = client.chat.completions.create(
    model="YOUR_MODEL_NAME", # model = "deployment_name".
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "list out all the players in the indian national cricket team?"}
    ]
)

#printing the final response after making the API call
print("the information is:" + response.choices[0].message.content + "\n")
