from time import *
from requests import *
from pync import *
import json

env = open('.env', 'r')

uid = env.readline().strip()
secret = env.readline().strip()

#curl -X POST --data "grant_type=client_credentials&client_id=MY_AWESOME_UID&client_secret=MY_AWESOME_SECRET" https://api.intra.42.fr/oauth/token

token = ""
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
