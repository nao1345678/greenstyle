import requests
import pandas as pd

API_KEY = "mNm8lpEUIbPzJu5gHu9ieAtt"

url = "https://wikirate.org/Companies.json"
params = {
    "metric_name": "Living wage paid?",
    "project": "Fashion Checker",
    "api_key": API_KEY
}

headers = {"User-Agent": "YourAppName/1.0"}  

response = requests.get(url, headers=headers, params=params)

print("Status:", response.status_code)
if response.status_code == 200:
    data = response.json()
    
else:
    print("Erreur:", response.text[:500])


print(f"Living wage : {len(data)} lignes")

