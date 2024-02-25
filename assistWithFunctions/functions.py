import os
import openai
import json
import requests
import time
from openai import AzureOpenAI
import dotenv
from dotenv import load_dotenv
import pandas as pd
from IPython.display import clear_output

#defining a function for getting the stock price dataset of a particular company
def get_stock_price(company):
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+company+"&apikey="+os.getenv("ALPHA_VANTAGE_API_KEY")
    response = requests.get(url).json()
    volume = response['Time Series (Daily)']['2024-02-23']['5. volume']
    high = response['Time Series (Daily)']['2024-02-23']['2. high']
    low = response['Time Series (Daily)']['2024-02-23']['3. low']
    close  = response['Time Series (Daily)']['2024-02-23']['4. close']
    output_response = f"""here are some details of the stock price of the company {company}:
                date : 2024-02-23
                volume : {volume}
                high : {high}
                low : {low}
                close : {close}
                """
    return output_response
    
    

def main():
 load_dotenv()
    #creating azure openai client
 client = AzureOpenAI(
    api_key=os.getenv("API_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("ENDPOINT")
 )

 #creating an openai assistant
 assistant = client.beta.assistants.create(
    instructions="You are a stock bot. Use the provided functions to answer the questions/user queries",
    model = os.getenv("MODEL"),
    tools=[{
      "type": "function",
    "function": {
      "name": "get_stock_price",
      "description": "get the stock price of the company that the user is interested in",
      "parameters": {
        "type": "object",
        "properties": {
          "company": {
              "type": "string",
              "description": "the company whose stock price the user is interested in for instance 'IBM' or 'AAPL'"
              },
          
        },
        "required": ["company"]
        
      }
    }
  }]
 )
 thread = client.beta.threads.create()
 
 message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content = "provide me the stock data for IBM",
    
 )
 
 run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
  
 )
 
 run = client.beta.threads.runs.retrieve(
  thread_id=thread.id,
  run_id=run.id
 )
 
 status = run.status

 start_time = time.time()

 while status not in ["completed", "cancelled", "expired", "failed" , "requires_action"]:
    time.sleep(5)
    run = client.beta.threads.runs.retrieve(thread_id=thread.id,run_id=run.id)
    print("Elapsed time: {} minutes {} seconds".format(int((time.time() - start_time) // 60), int((time.time() - start_time) % 60)))
    status = run.status
    print(f'Status: {status}')
    clear_output(wait=True)

 if(status == "requires_action"):
     initial_response = json.loads(run.model_dump_json(indent=2))
     function_name = initial_response['required_action']['submit_tool_outputs']['tool_calls'][0]['function']['name']
     function_arguments = initial_response['required_action']['submit_tool_outputs']['tool_calls'][0]['function']['arguments']
     company_name = json.loads(function_arguments)['company']
     call_id=initial_response['required_action']['submit_tool_outputs']['tool_calls'][0]['id']
     func=globals().get(function_name)
     output = func(company_name)
     run = client.beta.threads.runs.submit_tool_outputs(
             thread_id=thread.id,
             run_id=run.id,
             tool_outputs=[{
                 "tool_call_id": call_id,
                 "output": output,
             }]
     )
     run=client.beta.threads.runs.retrieve(thread_id=thread.id,run_id=run.id)
     status=run.status
     while status not in ["completed", "cancelled", "expired", "failed" , "requires_action"]:
      time.sleep(5)
      run = client.beta.threads.runs.retrieve(thread_id=thread.id,run_id=run.id)
      status = run.status
      
 messages = client.beta.threads.messages.list(
  thread_id=thread.id
)
 
 final_message = json.loads(messages.model_dump_json(indent=2))
 print(final_message['data'][0]['content'][0]['text']['value'])
  



if __name__ == "__main__":
    load_dotenv()
    main()