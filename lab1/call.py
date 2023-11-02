#importing importing libraries
import os
import openai
from dotenv import load_dotenv

#setting openAI configurations
load_dotenv()
openai.api_type = "azure"
openai.api_base = os.getenv('OPENAI_API_BASE')
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv('OPENAI_API_KEY')

#Send request to Azure OpenAI model
response = openai.ChatCompletion.create(
    engine="prabhjotturbofm",
    temperature = 0.7,
    max_tokens=120,
    messages=[
        {"role":"system", "content":"Your are an assistant. Your work is to provide people with relevant and factual information"},
        {"role":"user", "content":"list out all the players in the Indian National Cricket Team"}
    ]
)

#printing the final response after making the API call
print("the information is:" + response.choices[0].message.content + "\n")