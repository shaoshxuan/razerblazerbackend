import requests
from config import *

api_str = '@razerhackathon.sandbox.mambu.com/api/'

def get_branch_key():
    req_str = get_api_str()
    req_str += 'branches/' + get_mambu_user()
    req = requests.get(req_str, auth=(get_mambu_user(),get_mambu_pw()))

    return req.json()["encodedKey"]

