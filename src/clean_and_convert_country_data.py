import pandas as pd
import json
import unidecode as ud
import re

def clean_and_convert_country_data(unclean_file_name):
    
    assert isinstance(unclean_file_name, str)
    
    regex = re.compile('[^a-zA-Z]')
    
    with open(r'\geographic_data\cities.json', encoding = 'utf8') as cities_raw:
        cities = json.loads(cities_raw.read())
    
    cities_dict = {regex.sub('', ud.unidecode(city['name'])).lower() : city['country_code'] for city in cities}
    
    with open(r'\geographic_data\countries.json', encoding = 'utf8') as countries_raw:
        countries = json.loads(countries_raw.read())
    
    countries_dict = {regex.sub('', ud.unidecode(country['name'])).lower() : country['iso2'] for country in countries}
    
    with open(r'\geographic_data\states.json', encoding = 'utf8') as states_raw:
        states = json.loads(states_raw.read())
    
    states_dict = {regex.sub('', ud.unidecode(state['name'])).lower() : state['country_code'] for state in states}
    
    user_data = pd.read_csv(unclean_file_name, index_col=1)
    
    raw_locations = list(user_data['location'])
    
    def search_for_location(location_string):
    
        country = None
        
        sections = location_string.split(',')
        
        sections = [regex.sub('', ud.unidecode(section)).lower() for section in sections]

        for split_words in reversed(sections):
            try:
                country = countries_dict[split_words]
                break
            except KeyError:
                try:
                    country = states_dict[split_words]
                    break
                except KeyError:
                    try:
                        country = cities_dict[split_words]
                        break
                    except KeyError:
                        country = 'Not Found'
        
        return country
    
    countries = [search_for_location(location) for location in raw_locations]
    
    user_data['countries'] = countries
    
    user_data.to_csv('users_with_country.csv')

