'''
Write a program that makes a PUT request to update your user information to a new first_name, last_name and email.

Again make a GET request to confirm that your information has been updated.

'''
import requests
from requests.sessions import should_bypass_proxies

base_url = "http://demo.codingnomads.co:8080/tasks_api/users"

# updated body content to change on server
body = {
    "id": 325,
    "first_name": "SCOTT",
    "last_name": "FORD",
    "email": "SWFORD@EMAIL.COM"
}

# making the put request
response_put = requests.put(base_url, json=body)

# print response code
print(f"Response code: {response_put.status_code}")

# get request for server data content
response_get = requests.get(base_url)

# print data content; updated entry at specified id should be here
print(f"Response content: {response_get.content}")
