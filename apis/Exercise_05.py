'''
Write a program that makes a DELETE request to remove the user your create in a previous example.

Again, make a GET request to confirm that information has been deleted.

'''
import requests

base_url = "http://demo.codingnomads.co:8080/tasks_api/users"

# specify ID of entry you want to delete
response_del = requests.delete(base_url + "/325")

# print status code
print(f"Response code: {response_del.status_code}")