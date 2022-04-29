import const

import urllib.request
import json
from datetime import datetime

def get_scopes():
    scopes = ''
    for scope in const.SCOPES:
        scopes = scopes + f'section:{scope}:read+'
    return scopes[:-1]

### needed stuff ###
token = None
section_id = None
term_id = None

#1. Get token
scopes = get_scopes()
print(scopes)
data = urllib.request.urlopen(f'{const.TOKEN_URL}?grant_type=client_credentials&client_id={const.CLIENT_ID}&client_secret={const.CLIENT_SECRET}&scope={scopes}').read()
token = json.loads(data)['access_token']
print(f'Got token: {token}')
print()

#2. Get section + term from User
req = urllib.request.Request('https://www.onlinescoutmanager.co.uk/oauth/resource', None, {"Authorization": f'Bearer {token}'})
data = urllib.request.urlopen(req).read()
user = json.loads(data)['data']
sections = user['sections']

for s in sections:
    if s['section_name'] == const.SECTION_NAME:
        print(f'Found section {s["section_name"]} ({s["section_id"]})')
        section_id = s['section_id']

        #now check for current term
        now = datetime.now()
        
        for term in s['terms']:
            start_date = datetime.fromisoformat(term['startdate'])
            end_date = datetime.fromisoformat(term['enddate'])

            if(now >= start_date and now <= end_date):
                print(f'Found correct term - {term["name"]} ({term["term_id"]})')
                term_id = term['term_id']
                break
        else:
            raise ValueError('No current term found')
        
        break
    else:
        raise ValueError('Section not found')

print()

