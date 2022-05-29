import json
from requests import Session
from tools import query_token


nga = Session()
nga_token = json.loads(query_token('nga'))
headers = nga_token['headers']
cookies = nga_token['cookies']
nga.headers.update(headers)
nga.cookies.update(cookies)
