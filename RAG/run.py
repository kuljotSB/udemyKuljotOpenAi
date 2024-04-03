#importing namespaces
import os
import openai
from openai import AzureOpenAI
import json
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

#setting important configurations
load_dotenv()
index_name="YOUR_INDEX_NAME_HERE"
endpoint = os.getenv('search_endpoint')
key = os.getenv('search_key')

#creating an Azure OpenAI client
openai_client = AzureOpenAI(
  azure_endpoint = os.getenv("oai_base"), 
  api_key=os.getenv("oai_key"),  
  api_version="2024-02-15-preview"
)

#setting important variables
max=0
lst=[]
sum=" "

#create an azure search client
credential = AzureKeyCredential(key)
client = SearchClient(endpoint=endpoint, index_name=index_name, credential=credential)

results = client.search(search_text="jee advanced 2023")

for result in results: 
    if result['@search.score']>max: #listing down only the keyphrases with the most confident search score
        max=result['@search.score']
        lst=result['keyphrases']



for keyphrases in lst: #parsing keyphrases from list data type to string data type so as to pass it as a query in the ChatCompletions API
    sum = sum + keyphrases + " "
    
prompt = "You are an AI assistant. You are given a set of keyphrases extracted from the pdf file of an engineering entrance examination's question paper. By making a note of all these keyphrases, list down all the important engineering topics such as fuild dynamics, thermodynamics etc. "

messages = [
    {"role":"system", "content": prompt},
    {"role":"user", "content":sum}
]

chat_response = openai_client.chat.completions.create(
    model="YOUR_MODEL_NAME",
    messages=messages
)

#printing the final response from the ChatCompletions API 
print(chat_response.choices[0].message.content)

