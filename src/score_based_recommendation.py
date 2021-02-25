import pandas as pd

# read & import data into pandas data frame
anime_data = "anime.csv"
# set maximum number of rows to 20 & define NaN identifiers
pd.set_option('max_rows', 20)
idntfrs = ['na', '-', '--', '?', 'None', 'none', 'non', '', 'Not available', ' ']
anime_df = pd.read_csv(anime_data, na_values=idntfrs)

# discard unwanted items
anime_df.drop(['status', 'aired_string', 'rank',
               'popularity', 'members'],
              axis=1, inplace=True)

# print('anime_df Shape:', anime_df.shape)
# print(anime_df.head())

# anime_df = anime_df.sort_values(by=['score'], ascending=False)
anime_df = anime_df[anime_df['scored_by'] > 100]
# display shape and rows of each data frame
# print('anime_df Shape:', anime_df.shape)
# print(anime_df.head())

# anime_df = anime_df.sort_values(by=['score'], ascending=False)
# print('anime_df Shape:', anime_df.shape)
# print(anime_df.head())


# print(anime_df.dtypes)

def get_score_based_recommendation(animes_to_recommend=10):
    # gets the n largest scores from the entire list
    #finds top scoring animes of all time
    animes_recommending = anime_df.nlargest(animes_to_recommend, 'score')
    recommendation = animes_recommending['title'].to_list()

    return recommendation


print(get_score_based_recommendation())
