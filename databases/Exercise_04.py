'''

Please create a new Python application that interfaces with a brand new database.
This application must demonstrate the ability to:

    - create at least 3 tables
    - insert data to each table
    - update data in each table
    - select data from each table
    - delete data from each table
    - use at least one join in a select query

BONUS: Make this application something that a user can interact with from the CLI. Have options
to let the user decide what tables are going to be created, or what data is going to be inserted.
The more dynamic the application, the better!


'''
import sqlalchemy
import os
from pprint import pprint

def menu_select():
    """get user to choose their database task"""

    user_menu = {
        1: 'Create a table.',
        2: 'Add data to a table.',
        3: 'Read data from a table.',
        4: 'Delete data from a table.',
        6: 'Done.'
    }

    for key, value in user_menu.items():
        print(f'{key}. {value}')

    user_choice = int(input('// Database Menu\n// Enter the number of the task you would like to perform:'))
    return user_choice

def table_column_datatype():
    """get title for table and columns; get datatype for columns"""

    # initialize list for titles, datatypes
    # initialize datatype selection menu
    column_titles_list = []
    column_datatype_list = []
    datatype_dict = {
        1: sqlalchemy.String(500),
        2: sqlalchemy.Integer(),
        3: sqlalchemy.Float(),
        4: sqlalchemy.Boolean()
    }

    # get the title of the table
    table_title = input('Enter a title for your table: ')

    # get the number of columns this table needs
    while True:
        try:
            column_amount = int(input(f'Enter the number of columns table {table_title.upper()} needs: '))
            break
        except ValueError:
            print('''
            Please enter a number for the amount of columns this table needs.
            ''')

    # get the title of the columns
    for num in range(1, column_amount + 1):
        column_title = input(f'Enter a title for Column #{num} in table {table_title.upper()}: ')
        column_titles_list.append(column_title)

    # specify the datatype of the columns
    for column in column_titles_list:
        # print datatype menu
        for num, datatype in datatype_dict.items():
            print(f'{num}. {datatype}')

        while True:
            try:
                column_datatype = int(input(f'Enter the number corresponding to the datatype that column {column.upper()} requires: '))
                # confirm user entered correct value      
                if column_datatype in datatype_dict.keys():
                    print(f'''
                    Confirmed: Column Title = {column.upper()} 
                    Confirmed: Datatype = {datatype_dict[column_datatype]}
                    ''')
                    # add the datetype to the list
                    column_object = datatype_dict[column_datatype]
                    column_datatype_list.append(column_object)
                    break
            except ValueError:
                print('''
                Please enter a number corresponding to your desired datatype.
                ''')
            except KeyError:
                print('''
                Please enter a valid number from the Datatype Menu
                ''')

    # create dictionary to use for table creation
    table_data_dict = {
        'table_title': table_title,
        'column_titles': column_titles_list,
        'column_datatypes': column_datatype_list,
    }
    
    return table_data_dict

def create_table(table_data_dict):
    """unpack values and create table"""

    column_args_list = []

    for num in range(len(table_data_dict['column_titles'])):
        column_set = sqlalchemy.Column(table_data_dict['column_titles'][num], table_data_dict['column_datatypes'][num])
        column_args_list.append(column_set)

    new_table = sqlalchemy.Table(
        table_data_dict['table_title'], metadata, *column_args_list)
    
    metadata.create_all(engine)
    return  

# set up MYSQL database connection
secret = os.environ['MYSQL_PASS']
engine = sqlalchemy.create_engine(f'mysql+pymysql://root:{secret}@localhost/TravelCompany')
connection = engine.connect()
metadata = sqlalchemy.MetaData()

# call functions
user_choice = menu_select()
table_data_dict = table_column_datatype()
create_table(table_data_dict)