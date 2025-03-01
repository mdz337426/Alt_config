import base64
from io import BytesIO
from dotenv import load_dotenv
import os
import requests
import time

load_dotenv()
api_key = os.getenv("api_key")

def get_response(image, prompt):
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}" 
    }

    payload = {
        "model": "gpt-4o",
        "messages": 
        [
            {
                "role": "user",
                "content": [
                    { "type": "text", "text": prompt},
                    { "type": "image_url","image_url": {"url": f"data:image/jpeg;base64,{image}" } } ]
            }    
        ],
        "max_tokens": 300
    }

    retries = 0
    max_retries = 5
    wait_time=2

    while retries < max_retries:
        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            data = response.json()
            print(data)
            content = data[0]['message']['content']
            return content
        except Exception as e:
            print(f"Attempt {retries+1} failed: {e}")
            retries+=1
            time.sleep(wait_time)
            wait_time+=1
    return "failed to fetch response after multiple attempts"


def get_response_with_file(sample_file, prompt):
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}" 
    }
    payload = {
        "model": "gpt-4o",
        "messages": 
        [

            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                    "type": "file",
                    "file_id": sample_file
                    }   
                                    
                    ]
            }    
        ],

        "max_tokens": 300
    }

    retries = 0
    max_retries = 5
    wait_time=2

    while retries < max_retries:
        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            data = response.json()
            print(data)
            content = data[0]['message']['content']
            return content
        except Exception as e:
            print(f"Attempt {retries+1} failed: {e}")
            retries+=1
            time.sleep(wait_time)
            wait_time+=1
    return "failed to fetch response after multiple attempts"





def generate_alt_text(examples, image_base64, prompt):
    """Generates alt text for an image using in-context learning."""
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": f"Use these Alt-Text for sample purpose as well as formatting style should be aligned according to these samples as well:\n {examples}"},
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
            ]}
        ],
        "max_tokens": 200
    }

    retries = 0
    max_retries = 5
    wait_time=2

    while retries < max_retries:
        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            data = response.json()
            print(data)
            content = data[0]['message']['content']
            return content
        except Exception as e:
            print(f"Attempt {retries+1} failed: {e}")
            retries+=1
            time.sleep(wait_time)
            wait_time+=1
    return "failed to fetch response after multiple attempts"
