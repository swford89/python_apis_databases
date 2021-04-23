'''
Building on the previous example, create a list of all of the emails of the users and print
the list to the console.

'''
import requests
from pprint import pprint

base_url = "http://demo.codingnomads.co:8080/tasks_api/users"

response = requests.get(base_url)

#pprint(response.text)

data_dict = response.json()
#print(data_dict)

email_list = []

for key in data_dict.keys():
    if type(data_dict[key]) == list:
        list_of_dicts = data_dict[key]
        for entry in list_of_dicts:
            for key in entry.keys():
                if key == "email":
                    email_list.append(entry[key])


for email in email_list:
    print(email)