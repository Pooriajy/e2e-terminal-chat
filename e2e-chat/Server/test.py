import requests
import json


url = 'http://127.0.0.1:8080/recv/'
data = {"msg":"this is a test", "sender":"mamad"}



x = requests.post(url,str(json.dumps(data)))

print(x.content)
