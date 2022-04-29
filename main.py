import const

import urllib.request
import json
from datetime import datetime

def get_scopes():
    scopes = ''
    for scope in const.SCOPES:
        scopes = scopes + f'section:{scope}:read+'
    return scopes[:-1]

def do_request(url):
    if token is not None:
        req = urllib.request.Request(url, None, {"Authorization": f'Bearer {token}'})
    else:
        req = url

    resp = urllib.request.urlopen(req).read()
    return json.loads(resp)

### needed stuff ###
token = None
section_id = None
term_id = None
rehearsal_date = '2022-04-28'

#1. Get token
scopes = get_scopes()
token = do_request(f'{const.TOKEN_URL}?grant_type=client_credentials&client_id={const.CLIENT_ID}&client_secret={const.CLIENT_SECRET}&scope={scopes}')['access_token']
print(f'Got token: {token}')
print()

#2. Get section + term from User
user = do_request('https://www.onlinescoutmanager.co.uk/oauth/resource')['data']
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

#3. Get attendance
members = do_request(f'https://www.onlinescoutmanager.co.uk/ext/members/attendance/?action=get&sectionid={section_id}&termid={term_id}')['items']
missing = []
for member in members:
    if not 'active' in member or not member['active'] or member['patrolid'] == -2:
        continue

    if not rehearsal_date in member:
        missing.append(member)
        
print(f'Found {len(missing)} missing members!')

#4. Get member details
for member in missing:
    print(f'Getting details for {member["firstname"]} {member["lastname"]}')
    details = do_request(f'https://www.onlinescoutmanager.co.uk/ext/customdata/?action=getData&section_id={section_id}&associated_id={member["scoutid"]}&associated_type=member&associated_is_section=null&varname_filter=null&context=members&group_order=section')['data']

    for detail in details:
        if detail["identifier"] == const.CONTACT_ID:

            for col in detail["columns"]:
                if col["column_id"] == const.CONTACT_PHONE_ID:
                    phone_number = col['value']
                    print(f'Found contact number, which is {phone_number}')
                    print('This is where we would text parents etc')
                    break
            else:
                raise ValueError('No phone number present')
            break
    else:
        raise ValueError('No contact present')
    
    print()
    
