import pandas as pd

# read & import data into pandas data frame
anime_user_data = "user_mal.csv"
anime_data = "anime.csv"
# set maximum number of rows to 20 & define NaN identifiers
pd.set_option('max_rows', 20)
idntfrs = ['na', '-', '--', '?', 'None', 'none', 'non', '', 'Not available', ' ']
# There is about 46 million reviews, but it lasts way way too long, so we are just
# using 1 million reviews from 5012 users
anime_user_df = pd.read_csv(anime_user_data, na_values=idntfrs, nrows=10000000)
anime_df = pd.read_csv(anime_data, na_values=idntfrs)

# drop unwanted members from anime_df to get only the id and the title
anime_df.drop(['status', 'aired_string', 'score',
               'scored_by', 'rank', 'members', 'popularity', 'genre'],
              axis=1, inplace=True)

# print(anime_user_df.head())
# print(anime_df.head())

# merge the two dataframes around their anime id
anime_combined_df = anime_user_df.merge(anime_df, on='anime_id')
# print(anime_combined_df.head())
# print(anime_combined_df.shape)

# move the data into a table where the columns are the anime title and the rows are indexed by
# username with values of scoring to make interpreting this data easier
anime_pivot_table = pd.pivot_table(anime_combined_df, index='username', columns='title', values='my_score')
# print(anime_pivot_table.head())
# print(anime_pivot_table.shape)


# Bad approach because Pearson’s Correlation Coefficient takes way too long to produce results
print(anime_pivot_table.corr()['One Piece'].sort_values(ascending=False).iloc[:20])
