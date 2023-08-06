import json

import requests

def post(body):
    r = requests.post('https://write.as/api/posts', data={'body': body})
    response = json.loads(r.text)
    return f'https://write.as/{response["data"]["id"]}.md'
