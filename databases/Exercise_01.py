'''

All of the following exercises should be done using sqlalchemy.

Using the provided database schema, write the necessary code to print information about the film and category table.

'''
import sqlalchemy
import os
from pprint import pprint

### pymysql
### cryptography

# Access virtual environment variable
secret = os.environ['MYSQL_PASS']

# create connection to database
# create relavent table objects
engine = sqlalchemy.create_engine(f'mysql+pymysql://root:{secret}@localhost/sakila')
connection = engine.connect()
metadata = sqlalchemy.MetaData()
film = sqlalchemy.Table('film', metadata, autoload=True, autoload_with=engine)
film_category = sqlalchemy.Table('film_category', metadata, autoload=True, autoload_with=engine)
category = sqlalchemy.Table('category', metadata, autoload=True, autoload_with=engine)

# join the tables
join_statement = film.join(
    film_category, film_category.columns.film_id == film.columns.film_id
    ).join(category, category.columns.category_id == film_category.columns.category_id)

# create the query for the films and their categories
query = sqlalchemy.select([film.columns.title, film.columns.rating, category.columns.name]).select_from(join_statement)

result_proxy = connection.execute(query)
result_set = result_proxy.fetchall()

pprint(result_set)