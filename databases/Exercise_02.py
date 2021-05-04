'''
Consider each of the tasks below as a separate database query. Using SQLAlchemy, which is the necessary code to:

1. Select all the actors with the first name of your choice

2. Select all the actors and the films they have been in

3. Select all the actors that have appeared in a category of a comedy of your choice

4. Select all the comedic films and sort them by rental rate

5. Using one of the statements above, add a GROUP BY statement of your choice

6. Using one of the statements above, add a ORDER BY statement of your choice

'''
import sqlalchemy
from sqlalchemy import func
import os
from pprint import pprint

### pymysql
### cryptography

secret = os.environ['MYSQL_PASS']

engine = sqlalchemy.create_engine(f'mysql+pymysql://root:{secret}@localhost/sakila')
connection = engine.connect()
metadata = sqlalchemy.MetaData()
actor = sqlalchemy.Table('actor', metadata, autoload=True, autoload_with=engine)
film_actor = sqlalchemy.Table('film_actor', metadata, autoload=True, autoload_with=engine)
film = sqlalchemy.Table('film', metadata, autoload=True, autoload_with=engine)
film_category = sqlalchemy.Table('film_category', metadata, autoload=True, autoload_with=engine)
category = sqlalchemy.Table('category', metadata, autoload=True, autoload_with=engine)

# 1. Select all the actors with the first name of your choice
name_query = sqlalchemy.select([actor]).where(actor.columns.first_name == 'WOODY')

# 2. Select all the actors and the films they have been in
actor_film_join = actor.join(
    film_actor, film_actor.columns.actor_id == actor.columns.actor_id
    ).join(film, film.columns.film_id == film_actor.columns.film_id)

actor_film_query = sqlalchemy.select(
    [film.columns.title, film.columns.release_year, actor.columns.first_name, actor.columns.last_name]
    ).select_from(actor_film_join)

# 5. Using one of the statements above, add a GROUP BY statement of your choice
film_count_query = sqlalchemy.select(
    [sqlalchemy.func.count(actor.columns.actor_id), actor.columns.first_name, actor.columns.last_name]
    ).select_from(actor_film_join).group_by(actor.columns.actor_id)

# 3. Select all the actors that have appeared in a category of a comedy of your choice
comedy_film_join = actor.join(
    film_actor, film_actor.columns.actor_id == actor.columns.actor_id
    ).join(film, film.columns.film_id == film_actor.columns.film_id
    ).join(film_category, film_category.columns.film_id == film.columns.film_id
    ).join(category, category.columns.category_id == film_category.columns.category_id)

comedy_film_query = sqlalchemy.select(
    [film.columns.title, film.columns.release_year, actor.columns.first_name, actor.columns.last_name]
    ).select_from(comedy_film_join).where(film.columns.title == 'MEMENTO ZOOLANDER')

# 4. Select all the comedic films and sort them by rental rate
comedy_rental_join = film.join(film_category, film_category.columns.film_id == film.columns.film_id
    ).join(category, category.columns.category_id == film_category.columns.category_id)

comedy_rental_query = sqlalchemy.select(
    [film.columns.title, film.columns.rental_rate, category.columns.name]
    ).select_from(comedy_rental_join)

# 6. Using one of the statements above, add a ORDER BY statement of your choice
rental_orderby_query = sqlalchemy.select(
    [film.columns.title, film.columns.rental_rate, category.columns.name]
).select_from(comedy_rental_join).order_by(sqlalchemy.asc(film.columns.rental_rate))

query_dict = {
    1: name_query,
    2: actor_film_query,
    3: comedy_film_query,
    4: comedy_rental_query,
    5: film_count_query,
    6: rental_orderby_query
}

result_proxy = connection.execute()         # enter in query_dict[#] to execute the query you'd like
result_set = result_proxy.fetchall()

pprint(result_set)