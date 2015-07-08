from urllib import request, parse, error

import json
from pprint import pprint
import random

def fetch_data(url, params, method):

    if method=='POST':
        data = json.dumps(params).encode('utf-8')
        req = request.Request(url)
        req.add_header("Content-Type","application/json;charset=utf-8")
        response = request.urlopen(req, data)
    else:
        params = parse.urlencode(params)
        response = request.urlopen(url+'?'+params)
    return (json.loads(response.read().decode('utf-8')), response.code)


url = 'https://flask-registration.herokuapp.com/api/users'
url = 'http://localhost:5000/api/users'



print('Currently evaluable users')
users = fetch_data(url, {}, 'GET')
pprint([user['email'] for user in users[0]['users']])
print("number of users  %d" % (len(users[0]['users'])))
print()




# add new user
# user data is incorrect
new_user ={
    'email': 'mail' + str(random.randint(0, 10000)),
    'password': 'qwerty',
    'other': 'tel. +180111111111111'
}

print('Register new user, email is incorrect')
try:
    pprint(fetch_data(url, new_user, 'POST'))
except error.HTTPError as e:
    print(e, e.read().decode('utf-8'))
print()



# user data is correct
new_user ={
    'email': 'mail' + str(random.randint(0, 10000))+ '@mail.com',
    'password': 'qwerty',
    'other': 'tel. +180111111111111'
}



print('Register new user, email is correct')
try:
    pprint(fetch_data(url, new_user, 'POST'))
except error.HTTPError as e:
    print(e, e.read().decode('utf-8'))
print()



users = fetch_data(url, {}, 'GET')
print("number of users now %d \n" % (len(users[0]['users'])))


print("get users ordered by email")
users = fetch_data(url, {'sort': 'email'}, 'GET')
pprint([user['email'] for user in users[0]['users']])
print()



print("get users ordered by date in desc order")
users = fetch_data(url, {'sort': '-date'}, 'GET')
pprint([(user['email'], user['timestamp']) for user in users[0]['users']])
print()
