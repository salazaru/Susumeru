# import libraries
import pandas as pd
import numpy as np

# assign csv data urls
# anime_data    = 'https://f000.backblazeb2.com/file/mal-db/AnimeList.csv'
# user_data     = 'https://f000.backblazeb2.com/file/mal-db/UserList.csv'
# user_mal_data = 'https://f000.backblazeb2.com/file/mal-db/UserAnimeList.csv'

# local directory
anime_data    = 'C:\\Users\\Uri\\Desktop\\data\\AnimeList.csv'
user_data     = 'C:\\Users\\Uri\\Desktop\\data\\UserList.csv'
#user_mal_data = 'C:\\Users\\Uri\\Desktop\\data\\UserAnimeList.csv'

# set maximum number of rows to 20 & define NaN identifiers
pd.set_option('max_rows', 20)
idntfrs = ['na', '-', '--', '?', 'None', 'none', 'non', '', ' ', \
           'Not available', '0']

# define chunk size for user_mal_data since the file is too large
# my_chunk = 10**4

# read & import data into pandas data frames
anime_df    = pd.read_csv(anime_data, na_values=idntfrs)
user_df     = pd.read_csv(user_data, na_values=idntfrs)
#user_mal_df = pd.read_csv(user_mal_data, na_values=idntfrs)

# since UserAnimeList.csv is too large, read it from a generator in chunks
# user_mal_gen = pd.read_csv(user_mal_data, na_values=idntfrs, iterator=True, \
#                            chunksize = my_chunk)
# user_mal_df  = next(user_mal_gen)

# display shape and rows of each data frame
# print('anime_df Shape:', anime_df.shape)
# anime_df.head()

# print('user_df Shape:', user_df.shape)
# user_df.head()

# print('user_mal_df Shape:', user_mal_df.shape)
# user_mal_df.head()

# drop unwanted features from the anime data frame
anime_df.drop(['title_english', 'title_japanese', 'title_synonyms', \
 			   'image_url', 'type', 'source', 'episodes', 'airing', 'aired', \
 			   'duration', 'rating', 'broadcast', 'related', \
 			   'producer', 'licensor', 'premiered', 'studio', 'opening_theme', \
 			   'ending_theme', 'background', 'favorites'], axis=1, inplace=True)

anime_df.dropna(inplace=True)

# fix broken apostrophes across the entire dataframe
# anime_df.replace('&#039;', '\'', inplace=True)
anime_df['title'] = anime_df['title'].str.replace('&#039;', '\'')

# remove animes that have not yet aired since they don't have scoring data
# anime_df = anime_df[~anime_df['status'].isin(['Not yet aired'])]

# remove NSFW content
# anime_df = anime_df[~anime_df['genre'].astype(str).str.contains('Hentai')]

# convert genres to a list
# anime_df['genre'] = anime_df.genre.str.split(',')

# write cleaned data frame to csv file for AnimeList.csv
anime_df.to_csv('anime.csv', index=False) 
print('anime_df Shape:', anime_df.shape)
anime_df.isna().sum()

drop unwanted features from the user data frame
user_df.drop(['user_watching', 'user_completed', 'user_onhold', 'user_dropped' \
              'user_plantowatch', 'user_days_spent_watching', 'access_rank', \
              'join_date', 'last_online', 'stats_mean_score', \
              'stats_rewatched', 'stats_episodes'], axis=1, inplace=True)

user_df.dropna(inplace=True)

# write cleaned data frame to csv file for UserList
user_df.to_csv('user.csv', index=False)
print('user_df Shape:', user_df.shape)
suer_df.isna().sum()



