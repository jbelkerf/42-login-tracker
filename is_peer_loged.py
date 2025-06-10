from time import *
from requests import *
from pync import *
import json

env = open('.env', 'r')

uid = env.readline().strip()
secret = env.readline().strip()

def get_token():
    url = "https://api.intra.42.fr/oauth/token"
    data = {'grant_type': 'client_credentials', 'client_id': uid, 'client_secret': secret}
    response = post(url, data=data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print("Failed to get token")
        return None

token = get_token()
print(f"Token: {token}")
user_to_track = 'jbelkerf'
url =  f"https://api.intra.42.fr/v2/users/{user_to_track}"
headers = {f"Authorization": {token}}

notify("anxdk nfr3K\n", title = "bsssss")
while True:
    req = get(url, headers=headers)
    user = json.loads(req.content.decode())
    
    # print(req.content.decode())
    if user['location'] == None:
        print("not loged")
    else:
        notify(f"Peer login detected in {user['location']}!", title="the MF loged in!")
        # break 
    sleep(50)
