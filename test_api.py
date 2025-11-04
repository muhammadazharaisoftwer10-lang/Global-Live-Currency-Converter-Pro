import requests
print(requests.get("https://api.exchangerate.host/latest").json())
