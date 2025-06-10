from time import *
from requests import *
from pync import *
import json
import sys


def get_token():
    url = "https://api.intra.42.fr/oauth/token"
    data = {'grant_type': 'client_credentials', 'client_id': uid, 'client_secret': secret}
    response = post(url, data=data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print("Failed to get token")
        return None
def check_loged():
    while True:
        req = get(url, headers=headers)
        user = json.loads(req.content.decode())
        
        # print(req.content.decode())
        if user['location'] == None:
            print("not loged")
        else:
            notify(f"Peer login detected in {user['location']}!", title=f"the {user_to_track} loged in!")
            sleep(3)
            notify(f"Peer login detected in {user['location']}!", title=f"the {user_to_track} loged in!")
            break 
        sleep(10)

def check_deloged():
     while True:
        req = get(url, headers=headers)
        user = json.loads(req.content.decode())
        
        # print(req.content.decode())
        if user['location'] == None:
            notify("you mf deloged !", title=f"the {user_to_track} not loged in!")
            sleep(3)
            notify("you mf deloged !", title=f"the {user_to_track} not loged in!")
            break
        else:
            print("still loged...")
        sleep(10)
# Read the .env file for credentials
env = open('.env', 'r')
uid = env.readline().strip()
secret = env.readline().strip()

#Get the tpken to authenticate
token = get_token()

#get the user to track
if sys.argv[1] != '':
    user_to_track = sys.argv[1]
else:
    print("usage: ./launch.sh <user_to_track> <loged/deloged>")
    sys.exit(1)

# Set the URL for the user to track
url =  f"https://api.intra.42.fr/v2/users/{user_to_track}"
headers = {f"Authorization": f"Bearer {token}"}

#set the mode of tracking loged or deloged
if sys.argv[2] == 'loged':
    check_loged()
elif sys.argv[2] == 'deloged':
    check_deloged()
else:
    print("usage: ./launch.sh <user_to_track> <loged/deloged>")
    sys.exit(1)
