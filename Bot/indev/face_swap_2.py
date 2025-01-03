import http.client

conn = http.client.HTTPSConnection("api.piapi.ai")
payload = ''
headers = {
   'x-api-key': ''
}
conn.request("GET", "/api/v1/task/80f5285b-6a84-45b2-886e-eade8b0a10d9", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))