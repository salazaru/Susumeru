import pandas as pd

# read & import data into pandas data frame
anime_user_data = "user_mal.csv"
anime_data = "anime.csv"
user_data = "user_country_age.csv"
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

# print(anime_user_df.head())
# print(user_df.head())


def get_location_based_recommendation(location, animes_to_recommend=10):
    if location in user_df['country'].values:
        # get only the users that are within the specifie country
        location_user_df = user_df[user_df['country'] == location]
        # print(location_user_df.head())

        # get only the user reviews that are within the specified country based off username
        location_anime_user_df = anime_user_df[anime_user_df['username'].isin(location_user_df['username'].to_list())]
        # print(location_anime_user_df.head())

        # according to IMDB top 250 formula
        # weighted rank = (v/(v+k))*X + (k/(v+k))*C
        # X = average for the movie(mean)
        # v = number of votes for the movie
        # k = minimum votes required to be listed in the top 250
        # C = the mean vote across the whole report
        whole_mean = anime_user_df['my_score'].mean()
        min_votes = 50
        anime_votes = location_anime_user_df.groupby('anime_id')['my_score'].agg('count')

        location_anime_user_df = location_anime_user_df.pivot(index='anime_id', columns='username', values='my_score')
        anime_mean = location_anime_user_df.mean(axis=1)

        location_anime_df = anime_df
        location_anime_df['weighted_score'] = (anime_votes / (anime_votes + min_votes)) * anime_mean + \
                                              (min_votes / (anime_votes + min_votes)) * whole_mean

        # print(location_anime_df)
        location_anime_df.dropna(inplace=True)
        # print(location_anime_df)

        # print("recommending")
        animes_recommending = location_anime_df.nlargest(animes_to_recommend, 'weighted_score')
        recommendation = animes_recommending['title'].to_list()

        return recommendation
    else:
        return "Error. That country isn't in our database"


print(get_location_based_recommendation("United states"))
