'''
Write the necessary code to make a POST request to:

    http://demo.codingnomads.co:8080/tasks_api/users

and create a user with your information.

Make a GET request to confirm that your user information has been saved.

'''
import requests

base_url = "http://demo.codingnomads.co:8080/tasks_api/users"

body = {
    "first_name": "Scott2",
    "last_name": "Ford2",
    "email": "swford@email.com2"
}

# post user info to server
response_post = requests.post(base_url, json=body)
print(f"Response code: {response_post.status_code}")

# retrieve updated server content
response_get = requests.get(base_url)
print(f"Response Content: {response_get.content}")