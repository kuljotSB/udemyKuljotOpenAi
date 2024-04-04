#importing important utilities and libraries
import os
import requests
from openai import AzureOpenAI
import tiktoken
import PyPDF2
import math
from dotenv import load_dotenv

#function to count number of tokens using tiktoken function
def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def main():
    load_dotenv()
    #defining an azure openai client
    client = AzureOpenAI(
        azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
        api_key=os.getenv('AZURE_OPENAI_KEY'),
        api_version="2024-02-15-preview"
    )
     #reading text from the PDF Document
    user_prompt=""
    reader = PyPDF2.PdfReader('document.pdf')
    for pages in reader.pages:
        user_prompt = user_prompt+pages.extract_text()
    #get number of tokens from the PDF text
    no_of_tokens = num_tokens_from_string(user_prompt,"cl100k_base")
    #variable initialization
    summary=""
    word_sum=""
    
    n=math.ceil(no_of_tokens/4096)
    print(n)
    content_length = len(user_prompt)
    lcount=0
    print(content_length)
    rcount=int(content_length/n)
    print(rcount)
     #using the "chain of summarisation" alogorithm
    while(rcount<content_length):
        word_sum = user_prompt[lcount:rcount]
        response = client.chat.completions.create(
            model=os.getenv('MODEl'),
            messages=[
                {"role":"system","content":"You are an ai assistant designed to help people"},
                {"role":"user","content":"I am providing you with a content in english \n"
                                          "generate a summary of this content \n"
                                         + word_sum}
            ],
            temperature=0.7
        )
        summary = summary + response.choices[0].message.content
        lcount=int(lcount + content_length/n)
        rcount=int(rcount+content_length/n)
     #printing the final summary
    final_response=client.chat.completions.create(
        model=os.getenv('MODEL'),
        messages=[
            {"role":"system","content":"You are an ai assistant designed to help people"},
            {"role":"user","content":"Provide me with a summary of the following text that I am providing you with \n"
                                     + summary}
        ],
        temperature=0.7
    )
    
    final_summary = final_response.choices[0].message.content
    print(final_summary)
    
if(__name__=="__main__"):
    main()