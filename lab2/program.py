#importing important utilities and libraries
import json
import requests
import openai
import os
from dotenv import load_dotenv
from openai.embeddings_utils import get_embedding

#setting openai configuration details
load_dotenv()
openai.api_key = os.getenv('get_oai_key')
openai.api_base = os.getenv('get_oai_base')
openai.api_version = "2023-03-15-preview"
deployment_name = os.getenv('get_embed_model')
openai.api_type = "azure"

data="a lot of festivals are coming"

embedding=get_embedding(data, engine=deployment_name)

print(embedding)



