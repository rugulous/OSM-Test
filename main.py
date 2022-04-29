import const

import urllib.request
import json

def get_scopes():
    scopes = ''
    for scope in const.SCOPES:
        scopes = scopes + f'section:{scope}:read+'
    return scopes[:-1]

#1. Get token
scopes = get_scopes()
print(scopes)
data = urllib.request.urlopen(f'{const.TOKEN_URL}?grant_type=client_credentials&client_id={const.CLIENT_ID}&client_secret={const.CLIENT_SECRET}&scope={scopes}').read()
token = json.loads(data)['access_token']
print(f'Got token: {token}')
print()

#2. Get User
req = urllib.request.Request('https://www.onlinescoutmanager.co.uk/oauth/resource', None, {"Authorization": f'Bearer {token}'})
data = urllib.request.urlopen(req).read()
user = json.loads(data)
print(user)
print()

