import requests
import json
from dotenv import load_dotenv
import os
import http.client
import asyncio

load_dotenv()
API_KEY = os.environ.get('FACE_SWAP_API_KEY_MURAT')
# API_KEY = 'a6622b15868f57f6de5133d4c57d09724eaf6724023beed9ff5dcd51538f7122'


async def run_face_swap(main_img_base64: str, face_img_url_base64: str) -> str:
    url = "https://api.piapi.ai/api/v1/task"

    payload = json.dumps({
        "model": "Qubico/image-toolkit",
        "task_type": "face-swap",
        "input": {
            "target_image": main_img_base64,
            "swap_image": face_img_url_base64
        }
    })
    headers = {
        'x-api-key': API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # flag = 1
    left_time = 0
    res_url = None
    while True:
        try:
            task_id = response.json()['data']['task_id']
            url = "https://api.piapi.ai/api/v1/task/" + task_id

            payload = {}
            headers = {
                'x-api-key': API_KEY
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            res_url = response.json()['data']['output']['image_url']
            break
        except Exception as e:
            await asyncio.sleep(0.5)
            left_time += 0.5
            if left_time == 20:
                break

    return res_url