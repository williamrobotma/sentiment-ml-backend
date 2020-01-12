import requests
import json
from pprint import pprint

# Request Parameters
store = "android"       # Could be either "android" or "itunes".
language = "en"         # Two letter language code.

req_params = {"language": language}

# Auth Parameters
username = "745feecb53c7e695eb8e09e1337d295fbf535ec8"  # Replace {API_KEY} with your own API key.
password = "X"          # Password can be anything.

# Request URL
url = "https://api.appmonsta.com/v1/stores/%s/reviews.json" % store

# This header turns on compression to reduce the bandwidth usage and transfer time.
headers = {'Accept-Encoding': 'deflate, gzip'}

response = requests.get(url,
                        auth=(username, password),
                        headers=headers,
                        params=req_params,
                        stream=True)

print(response.status_code)
for line in response.iter_lines():
  # Load json object and print it out
  json_record = json.loads(line)
  pprint(json_record)
print(type(json_record))
print(len(json_record))