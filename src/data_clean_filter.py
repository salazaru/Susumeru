from datetime import date
import pandas as pd
import numpy as np
# import geonamescache
from collections import defaultdict
import string

# function definitions
def calculate_age(born):
    if type(born) != int:
        try:
            born = datetime.strptime(born, '%Y-%m-%d').date()
            today = date.today()
            if (today.month, today.year) < (born.month, born.year):
                age = (today.year - born.year) - 1
            else:
                age = today.year - born.year

            return age
        except:
            print('corrupt data')
            return 0
    
# compare each element in 'user location' with each possible city or country
# note: this method can be enhanced with regex

# note: a 'states' database needs to be added
# this would assign many users the USA

# as of now, this method will only assign a user with a country if an exact
# city/country name is specified by the user and that city/country exists in
# the 'worldcities' csv data file
def assign_country(location, user_row):
    print('assigning country for row:', user_row)
    
    # if locatation was a replaced nan value, skip this row
    if location == 0:
        return
    
    for word in location:
        for city_list in cities_df[['city']]:
            city_obj = cities_df[city_list]
            city_row = 0
            for city in city_obj.values:
                if word.strip() == city or \
                word.strip() == cities_df.at[city_row, 'country']:
                    temp = []
                    temp.append(cities_df.loc[city_row, 'country'])
                    user_df.loc[user_row, 'location'] = temp[0]
                    return
                city_row += 1

                
# assign csv data urls
# anime_data    = 'https://f000.backblazeb2.com/file/mal-db/AnimeList.csv'
# user_data     = 'https://f000.backblazeb2.com/file/mal-db/UserList.csv'
# user_mal_data = 'https://f000.backblazeb2.com/file/mal-db/UserAnimeList.csv'

# local directory
anime_data    = 'C:\\Users\\Uri\\Desktop\\data\\AnimeList.csv'
user_data     = 'C:\\Users\\Uri\\Desktop\\data\\UserList.csv'
user_mal_data = 'C:\\Users\\Uri\\Desktop\\data\\UserAnimeList.csv'

cities = 'worldcities.csv'

# set maximum number of rows to 20 & define NaN identifiers
pd.set_option('max_rows', 20)
idntfrs = ['na', '-', '--', '?', 'None', 'none', 'non', '', ' ', \
           'Not available', '0', '0000-00-00', 'NaT']

# read & import data into pandas data frames
anime_df    = pd.read_csv(anime_data, na_values=idntfrs)
user_df     = pd.read_csv(user_data, na_values=idntfrs)
cities_df   = pd.read_csv(cities)

# my_reader = pd.read_csv(user_mal_data, chunksize=my_chunk, iterator=True)
# user_mal_df = pd.concat(my_reader, ignore_index=True)

# since UserAnimeList.csv is too large, read it from a generator in chunks
# user_mal_gen = pd.read_csv(user_mal_data, na_values=idntfrs, iterator=True, \
#                            chunksize = my_chunk)
# user_mal_df  = next(user_mal_gen)

# read in user_data in small chunks for testing country methods...
# my_chunk = 1000
# user_gen = pd.read_csv(user_data, na_values=idntfrs, iterator=True, \
#                            chunksize = my_chunk)
# user_df  = next(user_gen)


# display shape and rows of each data frame
# print('anime_df Shape:', anime_df.shape)
# anime_df.head()

# print('user_df Shape:', user_df.shape)
# user_df.head()

# print('user_mal_df Shape:', user_mal_df.shape)
# user_mal_df.head()

# drop unwanted features from the data frames
anime_df.drop(['title_english', 'title_japanese', 'title_synonyms', \
               'image_url', 'type', 'source', 'episodes', 'airing', 'aired', \
               'duration', 'rating', 'broadcast', 'related', \
               'producer', 'licensor', 'premiered', 'studio', 'opening_theme', \
               'ending_theme', 'background', 'favorites'],
               axis=1, inplace=True)

user_df.drop(['user_watching', 'user_completed', 'user_onhold', 'user_dropped', \
              'user_plantowatch', 'user_days_spent_watching', 'access_rank', \
              'join_date', 'last_online', 'stats_mean_score', 'stats_rewatched', \
              'stats_episodes'],
               axis=1, inplace=True)

#user_df.drop(['location'], axis=1, inplace=True)

# convert location to a list of lowercase, alphabetical strings
user_df['location'] = user_df.location.str.lower()
user_df['location'] = user_df.location.str.split(',')

#delchars = string.punctuation
# delchars = ''.join(c for c in map(chr, range(256)) if not c.isalpha())

# user_df['location'] = user_df.location.str.translate(None, delchars)


#user_df['location'] = ''.join(ch for ch in user_df.location.str if ch.isalpha())


cities_df.drop(['city', 'lat', 'lng', 'iso2', 'iso3', \
                'admin_name', 'capital', 'population', 'id'],
                 axis=1, inplace=True)
cities_df.rename(columns={'city_ascii': 'city'}, inplace=True)
cities_df['city'] = cities_df.city.str.lower()
cities_df['country'] = cities_df.country.str.lower()


# print('cities:')
# for column in cities_df[['city']]:
#     column_obj = cities_df[column]
#     for city in column_obj.values:
#         print(city)

# print('locations:')
# for column in user_df[['location']]:
#     column_obj = user_df[column]
#     column_obj.dropna(inplace=True)
#     for location in column_obj.values:
#         print(location)

# user_df.dropna(inplace=True)
# for i in range(0, 50):
#      print(user_df.at[i, 'location'])



# assign each user's location with a country
# user_row = 0
# user_df.fillna(0, inplace=True)
# for column in user_df[['location']]:
#     column_obj = user_df[column]
#     column_obj.dropna(inplace=True)
#     for location in column_obj.values:    # this loop takes a while...
#         assign_country(location, user_row)
#         user_row += 1
# user_df.rename(columns={'location': 'country'}, inplace=True)
# user_df['country'] = user_df.country.str.capitalize()

# fix broken apostrophes across the entire dataframe
# anime_df.replace('&#039;', '\'', inplace=True)
anime_df['title'] = anime_df['title'].str.replace('&#039;', '\'')


# clean birth_date column so that it represents age as a number
# user_df['age'] = user_df['birth_date'].apply(calculate_age)
# user_df.drop('birth_date', axis=1, inplace=True)


# drop all N/A values from the data frames
# anime_df.dropna(inplace=True)
# user_df.dropna(inplace=True)
# user_df['age'] = user_df['age'].astype(int)



# clean location column so that it only list country
# gc = geonamescache.GeonamesCache()
# countries = gc.get_countries()
# print(countries)





# remove animes that have not yet aired since they don't have scoring data
# anime_df = anime_df[~anime_df['status'].isin(['Not yet aired'])]

# remove NSFW content
# anime_df = anime_df[~anime_df['genre'].astype(str).str.contains('Hentai')]

# convert genres to a list
# anime_df['genre'] = anime_df.genre.str.split(',')

# write cleaned data frames to csv files
# anime_df.to_csv('anime.csv', index=False)
# user_df.to_csv('user.csv', index=False)
# user_df.to_csv('user_country_age.csv', index=False)

#print('anime_df Shape:', anime_df.shape)
#anime_df.head()
#anime_df.isna().sum()

#print('user_df Shape:', user_df.shape)
#user_df.head()
# user_df.isna().sum()

# print('user_mal_df Shape:', user_mal_df.shape)
# user_mal_df.head()
# user_mal_df.isna().sum()

# define chunk size for user_mal_data since the file is too large
my_chunk = 10**6
i = 0
first_chunk = True
for chunk in pd.read_csv(user_mal_data, na_values=idntfrs,
                         chunksize=my_chunk, iterator=True):
    user_mal_df = chunk
    user_mal_df.drop(['my_watched_episodes', 'my_status', 'my_rewatching', \
                      'my_rewatching_ep', 'my_last_updated', 'my_tags', \
                      'my_finish_date'],
                      axis=1, inplace=True)
    user_mal_df.dropna(inplace=True)
    
#     # if a month or day is zero, set it to january 1st in order to not lose year
#     row = 0
#     for column in user_mal_df[['my_start_date']]:
#         column_obj = user_mal_df[column]
#         for date in column_obj.values:
#             if date[6] == '0' or date[9] == '0':
#                 s = list(date)
#                 s[6] = '1'
#                 s[9] = '1'
#                 cdate = ''.join(s)
#                 print(user_mal_df.loc[row, 'my_start_date'])
#                 user_mal_df.loc[row, 'my_start_date'] = cdate
#             row += 1
#             print('fixed row #:', row)
                
    # convert start date to datetime object and extract date
    user_mal_df['my_start_date'] = pd.to_datetime(user_mal_df['my_start_date'], errors='coerce')
    user_mal_df['year_watched'] = user_mal_df['my_start_date'].dt.year
    user_mal_df.dropna(inplace=True)
    user_mal_df.drop('my_start_date', axis=1, inplace=True)
    user_mal_df['year_watched'] = user_mal_df['year_watched'].astype(int)
    
    
    
    if first_chunk:   
        user_mal_df.to_csv('start_dates.csv', mode='w', header=True, index=False)
        first_chunk = False
    else:
        user_mal_df.to_csv('start_dates.csv', mode='a', header=False, index=False)
    
    i += 1
    print('processed', my_chunk*i, 'rows...')


#print('cities_df Shape:', cities_df.shape)
#cities_df.head()

# note: the final user_df is pretty depricated because only one 
# database is being used for location. 
# less users will be depricated when more location databases are added...
# user_df.head(100)
user_mal_df.head(20)