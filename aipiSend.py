import base64
import requests
import json

with open("image.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

json_data = {'image': encoded_string}

headers = {'Content-type': 'application/json'}
response = requests.post("http://127.0.0.1:5000/upload_image", data=json.dumps(json_data), headers=headers)

print(response.json())