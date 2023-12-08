#importing important utilities and libraries
import json
import requests
import openai
from openai import AzureOpenAI
import os
from dotenv import load_dotenv
from openai.embeddings_utils import get_embedding

#setting openai configuration details
load_dotenv()
deployment_name = os.getenv('get_embed_model')


#creating an Azure OpenAI client
client = AzureOpenAI(
  api_key = os.getenv("get_oai_key"),  
  api_version = "2023-05-15",
  azure_endpoint =os.getenv("get_oai_base") 
)

data="a lot of festivals are coming"

response = client.embeddings.create(
    input = data,
    model= "your_embedding_model_goes_here"
)


print(response.model_dump_json(indent=2))



