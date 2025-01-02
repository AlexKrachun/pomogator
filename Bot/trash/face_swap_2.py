import http.client

conn = http.client.HTTPSConnection("api.piapi.ai")
payload = ''
headers = {
   'x-api-key': 'a6622b15868f57f6de5133d4c57d09724eaf6724023beed9ff5dcd51538f7122'
}
conn.request("GET", "/api/v1/task/80f5285b-6a84-45b2-886e-eade8b0a10d9", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))