
face_swap_api_key = '53b5083e77634e89d420f18bdbce921ad43e1f94dc774a2655713cf752260f24'


import requests
import json

url = "https://api.piapi.ai/api/v1/task"

payload = json.dumps({
   "model": "Qubico/image-toolkit",
   "task_type": "face-swap",
   "input": {
      "target_image": "https://i.ibb.co/LnLYwhR/66f41e64b1922.jpg",
      "swap_image": "https://i.ibb.co/m9BFL9J/ad61a39afd9079e57a5908c0bd9dd995.jpg"
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