'''

Create an application that interfaces with the user via the CLI - prompt the user with a menu such as:

Please select from the following options (enter the number of the action you'd like to take):
1) Create a new account (POST)
2) View all your tasks (GET)
3) View your completed tasks (GET)
4) View only your incomplete tasks (GET)
5) Create a new task (POST)
6) Update an existing task (PATCH/PUT)
7) Delete a task (DELETE)

It is your responsibility to build out the application to handle all menu options above.


'''
import requests
from pprint import pprint

def http_request_select():
    """for making an HTTP Request"""
    while True:
        try:
            list_comp = [f"{key}. {value}" for key, value in http_request_dict.items()]
            for item in list_comp:
                print(item)
            task_number = int(input(f"\nTask Menu // Please enter a number for the task you'd like to perform: "))
            break
        except ValueError:
            print("Please enter a number for the action you'd like to take.")
    return task_number

def create_account(task_number):
    """1) Create a new account (POST)"""

    first_name = input("Enter you first name: ").capitalize()
    last_name = input("Enter your last name: ").capitalize()
    user_email = input("Enter your email: ")

    body = {
        "first_name": first_name,
        "last_name": last_name,
        "email": user_email,
    }

    response_post = requests.post(user_url, json=body)
    print(f"Response code for creating user account: {response_post.status_code}")

    response_get_confirm = requests.get(user_url)
    print(f"Response code for confirming addition of user: {response_get_confirm.status_code}")
    pprint(response_get_confirm.json())
    return

def get_all(task_number):
    """2) View all your tasks (GET)"""

    while True:
        try:
            user_id = int(input("Enter your User Id number: "))
            break
        except ValueError:
            print("Please enter a number.")

    all_tasks = requests.get(user_url + f"/{user_id}/tasks")
    print(f"Response code for get request: {all_tasks.status_code}")
    pprint(all_tasks.json())
    return

def get_complete(task_number):
    """3) View your completed tasks (GET)"""

    while True:
        try:
            user_id = int(input("Enter your User Id number: "))
            break
        except ValueError:
            print("Please enter a number.")

    params = {
        "userId": user_id,
        "complete": "true"
        }

    complete_get = requests.get(task_url, params=params)
    print(f"Response code for reading complete tasks: {complete_get.status_code}")
    pprint(complete_get.json())
    return

def get_incomplete(task_number):
    """4) View incomplete tasks (GET)"""

    while True:
        try:
            user_id = int(input("Enter your User Id number: "))
            break
        except ValueError:
            print("Please enter a number.")

    params = {
        "userId": user_id,
        "complete": "false"
    }

    incomplete_get = requests.get(task_url, params=params)
    print(f"Response code for reading incomplete tasks: {incomplete_get.status_code}")
    pprint(incomplete_get.json())
    return

def create_task(task_number):
    """5) Create new task (POST)"""

    while True:
        try:
            user_id = int(input("Enter your User Id: "))
            task_name = input("Enter in a title for your task: ")
            task_descript = input("Enter a short description of your task: ")
            break
        except ValueError:
            print("Please enter a number.")

    body = {
        "userId": user_id,
        "name": task_name,
        "description": task_descript,
    }

    task_posting = requests.post(task_url, json=body)
    print(f"Response code for task creation: {task_posting.status_code}")

    updated_task_get = requests.get(task_url)
    pprint(updated_task_get.json())
    return

def update_task(task_number):
    """6) Update an existing task (PATCH/PUT)"""

    while True:
        try:
            task_id = int(input("Enter you Task Id number: "))
            user_id = int(input("Enter your User Id number: "))
            task_name = input("Enter the name of the task you're updating: ")
            task_descript = input("Enter the description of your task: ")
            task_status = input("Is this task complete? Enter 'true' or 'false': ").lower()
            break
        except ValueError:
            print("Please enter only numbers for your task and user id.")

    body = {
        "id": task_id,
        "userId": user_id,
        "name": task_name,
        "description": task_descript,
        "completed": task_status,
    }

    task_putting = requests.put(task_url, json=body)
    print(f"Response code for updating task status: {task_putting.status_code}")

    updated_task_get = requests.get(task_url)
    data = updated_task_get.json()
    pprint(data)
    return

def delete_task(task_number):
    """7) Delete a task (DELETE)"""
    
    while True:
        try:
            task_id = int(input("Enter the Id of the task you'd like to delete: "))
            break
        except ValueError:
            print("Please enter a number for your Task Id.")

    task_delete = requests.delete(task_url + f"/{task_id}" )
    print(f"Response code for deleting your task: {task_delete.status_code}")

    updated_task_get = requests.get(task_url)
    pprint(updated_task_get.json())
    return

http_request_dict = {
    1: "Create a new account (POST)",
    2: "View all your tasks (GET)",
    3: "View your completed tasks (GET)",
    4: "View incomplete tasks (GET)",
    5: "Create new task (POST)",
    6: "Update an existing task (PATCH/PUT)",
    7: "Delete a task (DELETE)",
}

task_url = "http://demo.codingnomads.co:8081/tasks_api/tasks"
user_url = "http://demo.codingnomads.co:8081/tasks_api/users"

task_number = http_request_select()
if task_number in range(1,8):
    if task_number == 1:
        create_account(task_number)
    elif task_number == 2:
        get_all(task_number)
    elif task_number == 3:
        get_complete(task_number)
    elif task_number == 4:
        get_incomplete(task_number)
    elif task_number == 5:
        create_task(task_number)
    elif task_number == 6: 
        update_task(task_number)
    elif task_number == 7:
        delete_task(task_number)
else:
    print("There's no option with that number")