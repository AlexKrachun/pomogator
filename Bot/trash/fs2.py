face_swap_api_key = '53b5083e77634e89d420f18bdbce921ad43e1f94dc774a2655713cf752260f24'


import requests


task_id = 'd222aa49-f11c-4374-a3f2-213dd2a7097e'
url = "https://api.piapi.ai/api/v1/task/" + task_id

payload={}
headers = {
   'x-api-key': face_swap_api_key
}

response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)
res_url = response.json()['data']['output']['image_url']
print(res_url)

