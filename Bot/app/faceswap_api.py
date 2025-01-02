
import requests
import json
from dotenv import load_dotenv
import os


load_dotenv()
FACE_SWAP_API_KEY_ALEX = os.environ.get('FACE_SWAP_API_KEY_ALEX')


async def run_face_swap(main_img_url: str, face_img_url: str) -> str:
   
   main_img_url = 'https://cdnn21.img.ria.ru/images/155710/78/1557107817_0:0:3072:1728_1920x1080_80_0_0_5cdeb2ca82b2dce48b81213cadbe3249.jpg'
   face_img_url = 'https://i.pinimg.com/originals/a8/c7/8c/a8c78ce6f43cee9e48a3d6b2ff33f2f1.jpg'
   
   url = "https://api.piapi.ai/api/v1/task"
   payload = json.dumps({
      "model": "Qubico/image-toolkit",
      "task_type": "face-swap",
      "input": {
         "target_image": main_img_url,
         "swap_image": face_img_url
      }
   })
   print('p' * 100)
   print(payload)
   
   
   headers = {
      'x-api-key': FACE_SWAP_API_KEY_ALEX,
      'Content-Type': 'application/json'
   }
   
   response = requests.request("POST", url, headers=headers, data=payload)
   
   
   
   task_id = response.json()['data']['task_id']
   url = "https://api.piapi.ai/api/v1/task/" + task_id
   
   # payload={}
   # headers = {
   #    'x-api-key': FACE_SWAP_API_KEY_ALEX
   # }
   
   # response = requests.request("GET", url, headers=headers, data=payload)
   # print('-'*100)
   # print(response.json())
   # res_url = response.json()['data']['output']['image_url']
   # return res_url
   
   payload={}
   headers = {
      'x-api-key': FACE_SWAP_API_KEY_ALEX
   }

   response = requests.request("GET", url, headers=headers, data=payload)

   # print(response.text)
   res_url = response.json()['data']['output']['image_url']
   print(res_url)
   return res_url



   
# import json
# from dotenv import load_dotenv
# import os
# import aiohttp


# load_dotenv()
# FACE_SWAP_API_KEY_ALEX = os.environ.get('FACE_SWAP_API_KEY_ALEX')


# async def run_face_swap(main_img_url: str, face_img_url: str) -> str:
   
   
#    main_img_url = 'https://cdnn21.img.ria.ru/images/155710/78/1557107817_0:0:3072:1728_1920x1080_80_0_0_5cdeb2ca82b2dce48b81213cadbe3249.jpg'
#    face_img_url = 'https://i.pinimg.com/originals/a8/c7/8c/a8c78ce6f43cee9e48a3d6b2ff33f2f1.jpg'
         
#    url = "https://api.piapi.ai/api/v1/task"
   
   
#    payload = json.dumps({
#        "model": "Qubico/image-toolkit",
#        "task_type": "face-swap",
#        "input": {
#            "target_image": main_img_url,
#            "swap_image": face_img_url
#        }
#    })
   
#    headers = {
#        'x-api-key': FACE_SWAP_API_KEY_ALEX,
#        'Content-Type': 'application/json'
#    }
   
#    async with aiohttp.ClientSession() as session:
#        async with session.post(url, headers=headers, data=payload) as response:
#            response_data = await response.json()
#            task_id = response_data['data']['task_id']
       
#        url = "https://api.piapi.ai/api/v1/task/" + task_id
       
#        headers = {
#            'x-api-key': FACE_SWAP_API_KEY_ALEX
#        }
       
#        async with session.get(url, headers=headers) as response:
#            response_data = await response.json()
#            print('fuck' * 100)
#            print(response_data)
#            res_url = response_data['output']['image_url']
#            return res_url