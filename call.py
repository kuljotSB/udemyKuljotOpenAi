#importing importing libraries
import os
import openai

#setting openAI configurations
openai.api_type = "azure"
openai.api_base = os.getenv("azure_oai_endpoint")
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("azure_oai_key")

#Send request to Azure OpenAI model
response = openai.ChatCompletion.create(
    engine="YOUR_OAI_MODEL_HERE",
    temperature = 0.7,
    max_tokens=120,
    messages=[
        {"role":"system", "content":"Your are an assistant. Your work is to provide people with relevant and factual information"},
        {"role":"user", "content":"list out all the players in the Indian National Cricket Team"}
    ]
)

#printing the final response after making the API call
print("the information is:" + response.choices[0].message.content + "\n")