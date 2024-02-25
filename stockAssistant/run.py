#importing important utilities and libraries
import json
import requests
import matplotlib
import openai
import os
from IPython.display import clear_output
from openai import AzureOpenAI
from PIL import Image
import time
from dotenv import load_dotenv

#creating an Azure OpenAI client
load_dotenv()
client = AzureOpenAI(
    api_key=os.getenv("API_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("ENDPOINT")
)

#upload a file with the "assistants" purpose
file = client.files.create(
    file = open("./stockdataset.csv", "rb"),
    purpose = 'assistants'
)

#create an assistant
assistant = client.beta.assistants.create(
    name = "Stock Price Generator",
    instructions = f"You are a helpful AI assistant makes visualization of the stock price data that has been provided to you by the user"
    f" You have access to a sandboxed environment for writing and testing code"
    f" You can make use of all required pythonic libraries"
    f"When you are required to produce a data visualization, you should follow the following steps"
    f"1. Write the code"
    f"Run the code to confirm that it works"
    f"If the code is successful, display the visualization"
    f"if the code is unsuccessful, debug the code and run again",
    tools = [
        {"type":"code_interpreter"}
    ],
    model = os.getenv("model"),
    file_ids=[file.id]
)

#creating a thread
thread  = client.beta.threads.create()

#put the user message in the threaded conversation
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content = "create a visualization of the stock price data",
    file_ids=[file.id]
)

#running the thread
run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=assistant.id,
  
)

#retrieving the thread
run = client.beta.threads.runs.retrieve(
  thread_id=thread.id,
  run_id=run.id
)

status = run.status

start_time = time.time()

while status not in ["completed", "cancelled", "expired", "failed"]:
    time.sleep(5)
    run = client.beta.threads.runs.retrieve(thread_id=thread.id,run_id=run.id)
    print("Elapsed time: {} minutes {} seconds".format(int((time.time() - start_time) // 60), int((time.time() - start_time) % 60)))
    status = run.status
    print(f'Status: {status}')
    clear_output(wait=True)

messages = client.beta.threads.messages.list(
  thread_id=thread.id
)

print(messages.model_dump_json(indent=2))
output = json.loads(messages.model_dump_json(indent=2))

image_file_id = output['data'][0]['content'][0]['image_file']['file_id']
print(image_file_id)

content = client.files.content(image_file_id)
image= content.write_to_file("graph.png")

image= Image.open("graph.png")
image.show()
