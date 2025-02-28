import requests



# Step 1: Upload the file
# Replace with your actual file path



def upload_file(api_key, file_path):
    with open(file_path, "rb") as file:
        files = {
        "file": (file_path, file, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        }
        data = {
        "purpose": "assistants"  # Purpose must be defined
        }
        headers = {
        "Authorization": f"Bearer {api_key}"

        }
        response = requests.post("https://api.openai.com/v1/files", headers=headers, files=files, data=data)
    file_data = response.json()
    return file_data








# Step 2: Use the uploaded file in a threaded message
dt = """
headers["Content-Type"] = "application/json"

payload = {
    "model": "gpt-4o",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Here is the file for processing."
                },
                {
                    "type": "file",
                    "file_id": file_id
                }
            ]
        }
    ],
    "max_tokens": 300
}

#response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
#data = response.json()

print(data)

"""
