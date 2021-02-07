# import libraries
import pandas as pd

# assign csv data urls
anime_data = 'https://f000.backblazeb2.com/file/mal-db/AnimeList.csv'
user_data  = 'https://f000.backblazeb2.com/file/mal-db/UserList.csv'

# set maximum number of rows to 20 & define NaN identifiers
pd.set_option('max_rows', 20)
idntfrs = ['na', '-', '--', '?', 'None', 'none', 'non']

# read & import data into pandas data frames
anime_df = pd.read_csv(anime_data, na_values=idntfrs)
user_df  = pd.read_csv(user_data, na_values=idntfrs)

# display shape and rows of each data frame
# print('anime_df Shape:', anime_df.shape)
# anime_df.head()
# print('user_df Shape:', user_df.shape)
# user_df.head()

# drop unwanted features from the anime data frame
anime_df.drop(['title', 'title_japanese', 'title_synonyms', 'image_url',   \
              'type', 'source', 'episodes', 'airing', 'aired', 'duration', \
              'rating', 'broadcast', 'related', 'producer', 'licensor',    \
              'studio', 'opening_theme', 'ending_theme', 'background'],    \
              axis=1, inplace=True)

print('anime_df Shape:', anime_df.shape)
anime_df.head()

# drop unwanted features from the user data frame