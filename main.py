import json
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
import requests

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
  
image_path = "image.jpg"

base64_image = encode_image(image_path)

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}


# Use the OpenAI API to generate a CSV file
payload = {
  "model": "gpt-4o",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Analyze the uploaded image containing a petition and extract all the text present in the image. Then, convert the extracted text into a well-formatted CSV file, Ensure that the CSV file is organized with appropriate headers and separators for easy data manipulation. in your response only output that data that will go into the CSV file"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    }
  ],
  "max_tokens": 300
}

response = requests.post("https://api.openai.com/v1/chat/completions",headers=headers, json=payload)

print(response.json())
try:
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print(response.json())
except json.decoder.JSONDecodeError as e:
    print(f"JSONDecodeError: {e}")
    print(f"Response content: {response.content}")
csv_data = response.json()['choices'][0]['message']['content']

# Now write the CSV data to a file
with open('output.csv', 'w', newline='') as file:
    file.write(csv_data)

print("CSV file has been saved as 'output.csv'")