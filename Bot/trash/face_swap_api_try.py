import http.client
import json

conn = http.client.HTTPSConnection("api.piapi.ai")
payload = json.dumps({
   "model": "Qubico/image-toolkit",
   "task_type": "face-swap",
   "input": {
      "target_image": "https://opis-cdn.tinkoffjournal.ru/mercury/no-witcher-cover-in.ajhijjpwpxdc..jpg",
      "swap_image": "https://i.ibb.co/7Xvjj5P/image.jpg"
   }
})
headers = {
   'x-api-key': '',
   'Content-Type': 'application/json'
}
conn.request("POST", "/api/v1/task", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))

