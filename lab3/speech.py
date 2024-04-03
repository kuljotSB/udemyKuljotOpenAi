#importing important libraries and utilites for azure openAi model
import os
from openai import AzureOpenAI
import json
import requests
from dotenv import load_dotenv

#importing important libraries and utilities for azure speech service SDK
import azure.cognitiveservices.speech as speech_sdk


global speech_config
#loading speech configurations
load_dotenv()
speech_key = os.getenv('speechService_key')
speech_region = os.getenv('speechService_region')
    
#configuring speechConfig
speech_config = speech_sdk.SpeechConfig(speech_key,speech_region)
    
#get speech input
command = ''
    
#configure speech recognition
audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
speech_recognizer= speech_sdk.SpeechRecognizer(speech_config, audio_config)
print('start speaking....')
    
#process speech input
speech = speech_recognizer.recognize_once_async().get()
if speech.reason==speech_sdk.ResultReason.RecognizedSpeech:
    command=speech.text
print(command)

#creating an Azure OpenAI client
client = AzureOpenAI(
  azure_endpoint = os.getenv("oai_base"), 
  api_key=os.getenv("oai_key"),  
  api_version="2024-02-15-preview"
)

#sending the speech input as text to the system in the form of a prompt and then receiving the output through ChatCompletions function
response = client.chat.completions.create(
    model="YOUR_MODEL_NAME", # model = "deployment_name".
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": command}
    ]
)
    
print("the answer to your query is:" + response.choices[0].message.content + "\n")
    

    
    


    
            
                
    
        
    
