import pandas as pd


# read & import data into pandas data frame
anime_user_data = "user_mal.csv"
anime_data = "anime.csv"
user_data = "user_by_age.csv"
# set maximum number of rows to 20 & define NaN identifiers
pd.set_option('max_rows', 20)
idntfrs = ['na', '-', '--', '?', 'None', 'none', 'non', '', 'Not available', ' ']
# There is about 46 million reviews, but it lasts way way too long, so we are just
# using 1 million reviews from 5012 users
anime_user_df = pd.read_csv(anime_user_data, na_values=idntfrs, nrows=10000000)
anime_df = pd.read_csv(anime_data, na_values=idntfrs)
user_df = pd.read_csv(user_data, na_values=idntfrs)

# drop unwanted members from anime_df to get only the id and the title
anime_df.drop(['status', 'aired_string', 'score',
               'scored_by', 'rank', 'members', 'popularity', 'genre'],
              axis=1, inplace=True)
user_df.drop(['gender'], axis=1, inplace=True)

# print(anime_user_df.head())
# print(user_df.head())

# print(user_df.head())
# print(user_df.dtypes)
# print(anime_user_df.shape)


def get_location_based_recommendation(age, animes_to_recommend=10):
    age_user_df = user_df[user_df.iloc[:, 2].between(age - 5, age + 5, inclusive=False)]
    # print(location_user_df.head())
    # print(age_user_df.head())
    # print(age_user_df.shape)

    # omits all of the users from our review dataset that do not have a username in our age range
    age_user_df = anime_user_df[anime_user_df['username'].isin(age_user_df['username'].to_list())]

    # print(age_user_df.head())
    # print(age_user_df.shape)
    # print(age_user_df.head())
    # print(location_anime_user_df.head())

    # according to IMDB top 250 formula
    # weighted rank = (v/(v+k))*X + (k/(v+k))*C
    # X = average for the movie(mean)
    # v = number of votes for the movie
    # k = minimum votes required to be listed in the top 250
    # C = the mean vote across the whole report
    whole_mean = anime_user_df['my_score'].mean()
    min_votes = 50
    anime_votes = age_user_df.groupby('anime_id')['my_score'].agg('count')

    # make reading the graph and performing operations easier by grouping columns by username
    age_anime_user_df = age_user_df.pivot(index='anime_id', columns='username', values='my_score')
    anime_mean = age_anime_user_df.mean(axis=1)

    # adds the IMDB top 250 formula to each of the animes and adds that as a new column
    age_anime_df = anime_df
    age_anime_df['weighted_score'] = (anime_votes / (anime_votes + min_votes)) * anime_mean + \
                                          (min_votes / (anime_votes + min_votes)) * whole_mean

    # print(age_anime_df)
    # drops the animes that were not reviewed (aka not recommended by others in the age range)
    age_anime_df.dropna(inplace=True)
    # print(age_anime_df)

    # print("recommending")
    # getting the nth largest scores (high scored in that age range)
    animes_recommending = age_anime_df.nlargest(animes_to_recommend, 'weighted_score')
    recommendation = animes_recommending['title'].to_list()

    return recommendation


print(get_location_based_recommendation(20))
