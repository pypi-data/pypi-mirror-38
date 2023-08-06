# Write as anon
As simple as possible package to post on [write.as](https://write.as).

At current version you can only post as anonymous, and retrieve posts. Update, delete and any other operation are not supported (yet).

**Created to learn how to publish package on PyPi**

### Installation
As simple as:
```bash
pip install writeas-anon
```

### Usage
```python
from writeas_anon import post, build_url

text = '''# Hello world!
I've created a simple package called `writeas_anon`. You can find it [here](https://gitlab.com/chgrzegorz/writeas-anon)
I hope you will find this useful 😃'''

post_id = post(text)
print(build_url(post_id))
```
[https://write.as/1mky7cnx4ozq9.m](https://write.as/1mky7cnx4ozq9.md)
