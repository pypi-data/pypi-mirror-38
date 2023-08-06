import json

import requests


def post(body):
    """Send your post directly to write.as as anoynoymouse post."""
    r = requests.post('https://write.as/api/posts', data={'body': body})
    response = json.loads(r.text)
    return response["data"]["id"]


def get(post_id):
    """Get post from write.as
    If address of yout post is https://write.as/1mky7cnx4ozq9.md
    then id is 1mky7cnx4ozq9
    """
    r = requests.get(f'https://write.as/api/posts/{post_id}')
    response = json.loads(r.text)
    return response['data']


def build_url(post_id):
    return f'https://write.as/{post_id}.md'
