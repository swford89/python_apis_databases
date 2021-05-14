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
from sqlalchemy.exc import NoSuchTableError, NoSuchColumnError
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
    column_titles_list = []
    column_datatype_list = []

    # define the table
    table_title = input('Enter a title for your table: ')
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
                    Confirmed: Column title = {column.upper()} 
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
    while True:
        print(f'Column titles: {column_titles_list}')
        primary_key = input('Enter the title of the column you would like to set as the primary key: ')
        if primary_key in column_titles_list:
            break

    # create dictionary to use for table creation
    table_data_dict = {
        'table_title': table_title,
        'column_titles': column_titles_list,
        'column_datatypes': column_datatype_list,
        'primary_key': primary_key
    }
    
    return table_data_dict

def create_table(table_data_dict):
    """use data stored as dictionary to create table"""

    column_args_list = []

    for num in range(len(table_data_dict['column_titles'])):
        column_set = sqlalchemy.Column(table_data_dict['column_titles'][num], table_data_dict['column_datatypes'][num])
        if table_data_dict['primary_key'] == column_set.name:
            column_set = sqlalchemy.Column(table_data_dict['column_titles'][num], table_data_dict['column_datatypes'][num], primary_key=True)
            column_args_list.append(column_set)
        else:
            column_args_list.append(column_set)

    new_table = sqlalchemy.Table(table_data_dict['table_title'], metadata, *column_args_list)
    metadata.create_all(engine)
    print('''
    Table has successfully been created.
    ''')
    return  

def insert_data():
    """for inserting a NEW record into our database"""

    field_list = []
    column_title_list = []
    column_field_dict = {}

    # initialize the necessary table
    while True:
        try:
            table_title = input('Enter the name of the table you would like to add data to: ')
            specific_table = sqlalchemy.Table(table_title, metadata, autoload=True, autoload_with=engine)
            break
        except NoSuchTableError:
            print('''
            Your table either does not exist or is not spelled correctly. Try again.
            ''')

    # print column titles and class object type to promt user to choose datatype this column requires 
    for column in specific_table.columns:
        print(f'''
        Full column: {column}
        Column title: {column.name}
        Column datatype: {column.type}
        ''')

        # get field values the user wants to enter in
        while True:
            try:
                if isinstance(column.type, type(sqlalchemy.String())): 
                    field_value = input(f'Enter a string value for column {column.name.upper()}: ')
                    field_list.append(field_value)
                    column_title_list.append(column.name)
                    break
                elif isinstance(column.type, type(sqlalchemy.Integer())):
                    field_value = int(input(f'Enter an integer value for column {column.name.upper()}: '))
                    field_list.append(field_value)
                    column_title_list.append(column.name)
                    break
                elif isinstance(column.type, type(sqlalchemy.Float())):
                    field_value = float(input(f'Enter the float value for column {column.name.upper()}: '))
                    field_list.append(field_value)
                    column_title_list.append(column.name)
                    break
                elif isinstance(column.type, type(sqlalchemy.Boolean())):
                    field_value = bool(input(f'Enter a boolean value for column {column.name.upper()}'))
                    field_list.append(field_value)
                    column_title_list.append(column.name)
                    break
            except ValueError:
                print('Looks like you entered in an invalid datatype. Try again.')

    for index, title in enumerate(column_title_list):
            column_field_dict[title] = field_list[index]

    pprint(f'Dictionary of column titles and values to insert: {column_field_dict}')                

    insert_query = sqlalchemy.insert(specific_table).values(**column_field_dict)
    result_proxy = connection.execute(insert_query)
    print('''
    Insert Complete.
    ''')
    return

def update_data():
    """for updating an EXISTING record in our database"""

    # initialize the table
    while True:
        try:
            table_name = input('Enter the name of the table which contains your record: ')
            specific_table = sqlalchemy.Table(table_name, metadata, autoload=True, autoload_with=engine)
            break
        except NoSuchTableError:
            print('''
            Your table either does not exist or is not spelled correctly. Try again.
            ''')

    # define update data
    print(f'Column titles: {specific_table.columns.keys()}')
    update_column = input('Enter your update column: ')

    for column in specific_table.columns:
        while True:
            try:
                if update_column == column.name and isinstance(column.type, type(sqlalchemy.String())):
                    update_value = input('Enter your updated string value: ')
                elif update_column == column.name and isinstance(column.type, type(sqlalchemy.Integer())):
                    update_value = int(input('Enter your updated integer value: '))
                elif update_column == column.name and isinstance(column.type, type(sqlalchemy.Float())):
                    update_value = int(input('Enter your updated float value: '))
                elif update_column == column.name and isinstance(column.type, type(sqlalchemy.Boolean())):
                    update_value = int(input('Enter your updated boolean value: '))
            except ValueError:
                print('Looks like an invalid datatype was entered. Try again.')
            else:
                break
    update_dict = {update_column: update_value}

    # define where filter
    print(f'Column titles: {specific_table.columns.keys()}')
    where_column = input('Enter your where column: ')

    for column in specific_table.columns:
        while True:
            try:
                if column.name == where_column and isinstance(column.type, type(sqlalchemy.String())):
                    where_value = input('Enter your where-filter string value: ')
                elif column.name == where_column and isinstance(column.type, type(sqlalchemy.Integer())):
                    where_value = input('Enter your where-filter integer value: ')
                elif column.name == where_column and isinstance(column.type, type(sqlalchemy.Float())):
                    where_value = input('Enter your where-filter float value: ')
                elif column.name == where_column and isinstance(column.type, type(sqlalchemy.Boolean())):
                    where_value = input('Enter your where-filter boolean value: ')
            except ValueError:
                    print('Looks like an invalid datatype was entered. Try again.')
            else:
                break

    update_query = sqlalchemy.update(specific_table).values(**update_dict).where(
        specific_table.columns.where_column == where_value)  ### AttributeError
    result_proxy = connection.execute(update_query)
    print('''
    Update Complete.
    ''')
    return

def select_data():
    """for reading data from the database"""
    
    while True:
        try:
            table_name = input('Enter the name of the table you would like to read from: ')
            specific_table = sqlalchemy.Table(table_name, metadata, autoload=True, autoload_with=engine)
            break
        except NoSuchTableError:
            print('''
            Your table either does not exist or is not spelled correctly. Try again.
            ''')

    query = sqlalchemy.select([specific_table])
    result_proxy = connection.execute(query)
    result_set = result_proxy.fetchall()
    pprint(result_set)
    return

# set up MYSQL database connection
secret = os.environ['MYSQL_PASS']
engine = sqlalchemy.create_engine(f'mysql+pymysql://root:{secret}@localhost/TravelCompany')
connection = engine.connect()
metadata = sqlalchemy.MetaData()

# initialize datatype dict; global because multiple functions need to access it
datatype_dict = {
    1: sqlalchemy.String(500),
    2: sqlalchemy.Integer(),
    3: sqlalchemy.Float(),
    4: sqlalchemy.Boolean()
}

## call functions
# user_choice = menu_select()
# table_data_dict = table_column_datatype()
# create_table(table_data_dict)
# insert_data()
# update_data()
select_data()