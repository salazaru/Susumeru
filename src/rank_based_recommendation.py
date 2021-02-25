import pandas as pd

# read & import data into pandas data frame
anime_data = "anime.csv"
# set maximum number of rows to 20 & define NaN identifiers
pd.set_option('max_rows', 20)
idntfrs = ['na', '-', '--', '?', 'None', 'none', 'non', '', 'Not available', ' ']
anime_df = pd.read_csv(anime_data, na_values=idntfrs)

# discard unwanted items
anime_df.drop(['status', 'aired_string', 'score',
               'scored_by', 'members', 'popularity'],
              axis=1, inplace=True)

anime_df = anime_df.sort_values(by=['rank'], ascending=True)


def get_rank_based_recommendation(animes_to_recommend=10):
    # gets the n largest ranked animes
    # most popular animes of all time
    animes_recommending = anime_df.nlargest(animes_to_recommend, 'rank')
    recommendation = animes_recommending['title'].to_list()

    return recommendation


print(get_rank_based_recommendation())
