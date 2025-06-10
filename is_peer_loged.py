from time import *
from requests import *
import subprocess
import json
import sys
    

def notify(title, message):
    subprocess.run(['notify-send', title, message])

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
            notify("Heyyyyyy", f"The {user_to_track} is logged in {user['location']}.")
            break 
        sleep(10)

def check_deloged():
    while True:
        req = get(url, headers=headers)
        user = json.loads(req.content.decode())
        
        # print(req.content.decode())
        if user['location'] == None:
            notify("Heyyyyyy", f"The {user_to_track} is de-logged.")
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

if len(sys.argv) != 3:
    print("\033[31musage: ./launch.sh <user_to_track> <loged/deloged>\033[0m")
    sys.exit(1)
#get the user to track
if sys.argv[1] != '':
    user_to_track = sys.argv[1]
else:
    print("\033[31musage: ./launch.sh <user_to_track> <loged/deloged>\033[0m")
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
    print("\033[31musage: ./launch.sh <user_to_track> <loged/deloged>\033[0m")
    sys.exit(1)
