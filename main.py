import const

import urllib.request
import json

#1. Get token
data = urllib.request.urlopen(f'{const.TOKEN_URL}?grant_type=client_credentials&client_id={const.CLIENT_ID}&client_secret={const.CLIENT_SECRET}').read()
token = json.loads(data)['access_token']
print(f'Got token: {token}')
print()

#2. Get user details
req = urllib.request.Request('https://www.onlinescoutmanager.co.uk/oauth/resource', None, {"Authorization": f'Bearer {token}'})
data = urllib.request.urlopen(req).read()
user = json.loads(data)['data']
print(user)

