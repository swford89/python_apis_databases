'''
Use the countries API https://restcountries.eu/ to fetch information
on your home country and the country you're currently in.

In your python program, parse and compare the data of the two responses:
* Which country has the larger population?
* How much does the are of the two countries differ?
* Print the native name of both countries, as well as their capitals

'''
import requests
from requests.models import HTTPError, Response

def spell_check():
    """to confirm that search country is valid"""

    while True:     
        try:
            country_name = input("Enter the name of a country: ").lower()
            country_get = requests.get(base_url + country_name)
            Response.raise_for_status(country_get)
            break
        except requests.exceptions.HTTPError:
            print("""
            Spelling of the country looks to be incorrect. Try again.
            """)
    return country_name

def country_info(country_name):
    """for choosing what information you would like to access"""

    country_request = requests.get(base_url + country_name)
    country_data = country_request.json()

    for list_holding_dict in country_data:
        for key in list_holding_dict.keys():
            print(key)

    search_key = input("\nEnter the key you would like information on: ")
    print(f"""
    {list_holding_dict[search_key]}
    """)
    return

def country_essentials(country_name):
    """gives general non-technical information about the country"""

    country_request = requests.get(base_url + country_name)
    country_data = country_request.json()

    print(f"""General Information about: {country_name.capitalize()}:

    Population of {country_name.capitalize()}: {country_data[0]['population']:,}
    Capital City of {country_name.capitalize()}: {country_data[0]['capital']}
    """)
    return

def country_compare():
    """compare home country with another country"""
    while True:
        try:
            home_country = input("Enter the name of your home country: ").lower()
            another_country = input("Enter the name of another country you're interested in: ").lower()
            home_get = requests.get(base_url + home_country)
            home_data = home_get.json()
            another_get = requests.get(base_url + another_country)
            another_data = another_get.json()

            home_pop = home_data[0]['population']
            another_pop = another_data[0]['population']
            break
        except KeyError:
            print("""
            The spelling of a country doesn't seem to be right. Try again.
            """)

    if home_pop > another_pop:
        pop_diff = home_pop - another_pop
    elif another_pop > home_pop:
        pop_diff = another_pop - home_pop

    print(f"""
    {home_country.capitalize()} Population: {home_data[0]['population']:,}
    {home_country.capitalize()} Capital City: {home_data[0]['capital']}

    {another_country.capitalize()} Population: {another_data[0]['population']:,}
    {another_country.capitalize()} Capital City: {another_data[0]['capital']}

    Population Difference: {pop_diff:,}
    """)
    return

base_url = "https://restcountries.eu/rest/v2/name/"

country_name = spell_check()
country_info(country_name)
country_essentials(country_name)
country_compare()