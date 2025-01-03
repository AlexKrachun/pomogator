face_swap_api_key = '53b5083e77634e89d420f18bdbce921ad43e1f94dc774a2655713cf752260f24'
import requests

url = "https://api.piapi.ai/api/v1/task/" + '6433367f-8df5-448b-8c00-e4e31a27f81d'

payload={}
headers = {
   'x-api-key': face_swap_api_key
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)