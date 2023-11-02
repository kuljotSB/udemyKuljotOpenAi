#importing important libraries and utilites for azure openAi model
import os
import openai
import json
import requests

#importing important libraries and utilities for azure speech service SDK
import azure.cognitiveservices.speech as speech_sdk

def main():
    global speech_config
    #loading speech configurations
    speech_key = os.getenv('speechService_key')
    speech_region = os.getenv('speechService_region')
    
    #configuring speechConfig
    speech_config = speech_sdk.SpeechConfig(speech_key,speech_region)
    
    #get speech input
    command = speakInput()
    
    #loading openAi configurations
    openai.api_key = os.getenv('oai_key')
    openai.api_base = os.getenv('oai_base')
    openai.api_version = "2023-03-15-preview"
    openai.api_type="azure"
    
    #sending the speech input as text to the system in the form of a prompt and then receiving the output through ChatCompletions function
    response = openai.ChatCompletion.create(
        engine="YOUR_OAI_MODEL_HERE",
        temperature=0.7,
        tokens=120,
        messages=[
            {"role":"system", "content":"you are an assistant that helps people to fetch factual information"},
            { "role":"user", "content":command}
        ]
    )
    
    print("the answer to your query is:" + response.choices[0].message.content + "\n")
    
    

def speakInput():
    command = ''
    
    #configure speech recognition
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    speech_recognizer= speech_sdk.SpeechRecognizer(speech_config, audio_config)
    print('start speaking....')
    
    #process speech input
    speech = speech_recognizer.recognize_once_async().get()
    command=speech.text
    
            
                
    
        
    