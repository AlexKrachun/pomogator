
face_swap_api_key = '53b5083e77634e89d420f18bdbce921ad43e1f94dc774a2655713cf752260f24'


import requests
import json

url = "https://api.piapi.ai/api/v1/task"

payload = json.dumps({
   "model": "Qubico/image-toolkit",
   "task_type": "face-swap",
   "input": {
      "target_image": "https://api.telegram.org/file/bot7618816734:AAGKGYh_-wCZqTKlDyGY2GLHLoPZWoWJey4/photos/file_17.jpg",
      "swap_image": "https://api.telegram.org/file/bot7618816734:AAGKGYh_-wCZqTKlDyGY2GLHLoPZWoWJey4/photos/file_16.jpg"
   }
})
headers = {
   'x-api-key': face_swap_api_key,
   'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

# print(*response)
task_id = response.json()['data']['task_id']
print(task_id)


# import requests

# url = "https://api.piapi.ai/api/v1/task/"

# payload={}
# headers = {
#    'x-api-key': face_swap_api_key
# }

# response = requests.request("GET", url, headers=headers, data=payload)

# print(response)