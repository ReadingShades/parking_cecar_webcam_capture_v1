import requests
import json

url = "http://127.0.0.1:8000/api/v1/detections/"

payload = json.dumps({"src_file": "../test_img/test_08_IHT_214.jpg"})
headers = {"Content-Type": "application/json"}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
