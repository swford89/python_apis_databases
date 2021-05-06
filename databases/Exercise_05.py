'''
Using the API from the API section, write a program that makes a request to
get all of the users and all of their tasks.

Create tables in a new local database to model this data.

Think about what tables are required to model this data. Do you need two tables? Three?

Persist the data returned from the API to your database.

NOTE: If you run this several times you will be saving the same information in the table.
To prevent this, you should add a check to see if the record already exists before inserting it.

'''
import sqlalchemy
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.exc import IntegrityError as ie
import requests
import os

# create variables for urls and database access
secret = os.environ['MYSQL_PASS']
user_url = 'http://demo.codingnomads.co:8080/tasks_api/users'
task_url = 'http://demo.codingnomads.co:8080/tasks_api/tasks'

# get API info on users and tasks
user_response = requests.get(user_url)
task_response = requests.get(task_url)
user_data = user_response.json()
task_data = task_response.json()

# access DB and create tables for users and tasks
engine = sqlalchemy.create_engine(f'mysql+pymysql://root:{secret}@localhost/CodingNomads')
connection = engine.connect()
metadata = sqlalchemy.MetaData()

# create tables for user_data and task_data
user_table_create = sqlalchemy.Table(
    'users', metadata, 
    sqlalchemy.Column('user_id', sqlalchemy.Integer(), primary_key=True),            # user_id key different @ user endpoint == 'id'
    sqlalchemy.Column('first_name', sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column('last_name', sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column('email', sqlalchemy.String(255)),
    sqlalchemy.Column('createdAt', sqlalchemy.String(30)),                           # needs to be VARCHAR/String due to number length
    sqlalchemy.Column('updatedAt', sqlalchemy.String(30))                            # needs to be VARCHAR/String due to number length
)

tasks_table_create = sqlalchemy.Table(
    'tasks', metadata,
    sqlalchemy.Column('task_id', sqlalchemy.Integer(), primary_key=True, nullable=False),
    sqlalchemy.Column('user_id', sqlalchemy.Integer(), ForeignKey('users.user_id'), nullable=False),
    sqlalchemy.Column('name', sqlalchemy.String(255)),
    sqlalchemy.Column('description', sqlalchemy.String(500)),
    sqlalchemy.Column('createdAt', sqlalchemy.String(30)),
    sqlalchemy.Column('updatedAt', sqlalchemy.String(30)),
    sqlalchemy.Column('completed', sqlalchemy.Boolean()),
)

metadata.create_all(engine)

# initialize the created tables to insert into
user_table = sqlalchemy.Table('users', metadata, autolod=True, autoload_with=engine)
task_table = sqlalchemy.Table('tasks', metadata, autoload=True, autoload_with=engine)

# loop through user_data and enter user info into columns of users table in DB
for user in user_data['data']:
    insert_user_query = sqlalchemy.insert(user_table).values(
        user_id=user['id'], first_name=user['first_name'], last_name=user['last_name'], 
        email=user['email'], createdAt=user['createdAt'], updatedAt=user['updatedAt']
        )
    result_proxy = connection.execute(insert_user_query)

# create list for tasks that raised errors when trying to enter into DB
integrity_list = []

# loop through task_data and enter task info into columns of task table in DB
for task in task_data['data']:
    try:
        insert_task_query = sqlalchemy.insert(task_table).values(
            task_id=task['id'], user_id=task['userId'], name=task['name'],
            description=task['description'], createdAt=task['createdAt'], updatedAt=task['updatedAt'],
            completed=task['completed']
            )
        result_proxy = connection.execute(insert_task_query)
    # details for task and reason error was raised
    except sqlalchemy.exc.IntegrityError as ie:
        integrity_list.append(task)
        print(f'''
        {ie.orig}
        {ie.params}
        ''')