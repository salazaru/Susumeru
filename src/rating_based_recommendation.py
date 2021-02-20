import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# read & import data into pandas data frame
anime_data = "user_mal.csv"
# set maximum number of rows to 20 & define NaN identifiers
pd.set_option('max_rows', 20)
idntfrs = ['na', '-', '--', '?', 'None', 'none', 'non', '', 'Not available', ' ']
anime_df = pd.read_csv(anime_data, na_values=idntfrs)
anime_df

# discard unwanted items
# anime_df.drop(['status', 'aired_string', 'score',
#                'scored_by', 'members', 'popularity', 'rank'],
#               axis=1, inplace=True)

print(anime_df.head(3))