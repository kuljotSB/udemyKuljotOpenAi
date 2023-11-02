#importing important utilities and libraries
import os
import requests
import json
import openai

#import namespaces
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.conversations import ConversationAnalysisClient

#setting configurations
ls_endpoint = os.getenv('ls_endpoint')
ls_key = os.getenv('ls_key')

response=requests.post(url="https://kuljotlanguageresource.cognitiveservices.azure.com/language/:analyze-conversations?api-version=2022-10-01-preview", json={"text":"how is the manila hotel in india?"})
print(response.text)
                     
