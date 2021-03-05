import pandas as pd
from scipy import sparse
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

print("Initializing")
# read & import data into pandas data frame
anime_data = "anime.csv"
anime_user_data = "user_mal.csv"
location_user_data = "user_country_age.csv"
age_user_data = "user_by_age.csv"
# set maximum number of rows to 20 & define NaN identifiers
pd.set_option('max_rows', 20)
idntfrs = ['na', '-', '--', '?', 'None', 'none', 'non', '', 'Not available', ' ']

# There is about 46 million reviews, but it lasts way way too long, so we are just
# using 1 million reviews from 5012 users
# Read our datasets into dataframes from csv files
anime_df = pd.read_csv(anime_data, na_values=idntfrs)
anime_user_df = pd.read_csv(anime_user_data, na_values=idntfrs, nrows=10000000)
age_user_df = pd.read_csv(age_user_data, na_values=idntfrs)
location_user_df = pd.read_csv(location_user_data, na_values=idntfrs)


# drop unwanted members from our dataframes
anime_df.drop(['status', 'aired_string', 'members', 'popularity'],
              axis=1, inplace=True)

# score_anime_df = anime_df.drop(['rank'], axis=1, inplace=False)
#
# anime_df.drop(['score', 'scored_by'], axis=1, inplace=True)
#
# rank = anime_df.copy()
# score_anime_df = anime_df.drop(['status', 'aired_string', 'rank',
#                                 'popularity', 'members'],
#                                axis=1, inplace=False)
# anime_genre_df = anime_df.drop(['status', 'aired_string', 'score',
#                                 'scored_by', 'members', 'popularity', 'rank'],
#                                axis=1, inplace=False)
#
# anime_df.drop(['status', 'aired_string', 'score',
#                'scored_by', 'rank', 'members', 'popularity', 'genre'],
#               axis=1, inplace=True)

age_user_df.drop(['gender'], axis=1, inplace=True)


# score recommendation data prep **********************************
score_anime_df = anime_df[anime_df['scored_by'] > 100]
# *****************************************************************

# genre recommendation data prep **********************************
# separate the comma separated genres in the genre column
# and make each genre not case sensitive while also
# stripping away white space on the head/tail
anime_df['genre'] = anime_df['genre'].str.lower()
anime_df['genre'] = anime_df['genre'].str.replace(',', '')

# initialize a count vectorizer to have a vocabulary
# of the many genres we are feeding into this algorithm
count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(anime_df['genre'])

# use cosine similiarity to compare genres between animes
cos_sim = cosine_similarity(count_matrix, count_matrix)
# *****************************************************************

# rating based data preparation ***********************************
# pivot the dataframe so that we can more easily extract user interpretations
anime_user_rating_df = anime_user_df.pivot(index='anime_id', columns='username', values='my_score')

# Replacing all of the Nan value inputs with 0
anime_user_rating_df.fillna(0, inplace=True)

# reset the index so that we can search by index later
# when we want our recommendation
anime_user_rating_df.reset_index(inplace=True)

# save our sparsity matrix so that we can access it later
# to save time
# sparse.save_npz("csr_anime_user.npz", csr_anime_user)
csr_anime_user = sparse.load_npz("csr_anime_user.npz")

# KNN to find similarities/trends among users
# Using cosine metric as well as brute force algorithm in the interest of time
knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
knn.fit(csr_anime_user)
# *****************************************************************

# print("Ready")
def get_recommendations(age=None, location=None, anime=None, animes_to_recommend=10):
    recommendations = []

    if age is not None:
        # print('age recommending')
        age_user = age_user_df[age_user_df.iloc[:, 2].astype(int).between(age - 5, age + 5, inclusive=False)]

        # omits all of the users from our review dataset that do not have a username in our age range
        age_user = anime_user_df[anime_user_df['username'].isin(age_user['username'].to_list())]

        # according to IMDB top 250 formula
        # weighted rank = (v/(v+k))*X + (k/(v+k))*C
        # X = average for the movie(mean)
        # v = number of votes for the movie
        # k = minimum votes required to be listed in the top 250
        # C = the mean vote across the whole report
        age_whole_mean = anime_user_df['my_score'].mean()
        age_min_votes = 50
        age_anime_votes = age_user.groupby('anime_id')['my_score'].agg('count')

        # make reading the graph and performing operations easier by grouping columns by username
        age_anime_user_df = age_user.pivot(index='anime_id', columns='username', values='my_score')
        age_anime_mean = age_anime_user_df.mean(axis=1)

        # adds the IMDB top 250 formula to each of the animes and adds that as a new column
        age_anime_df = anime_df.copy(deep=True)
        age_anime_df['weighted_score'] = (age_anime_votes / (age_anime_votes + age_min_votes)) * age_anime_mean + (
                age_min_votes / (age_anime_votes + age_min_votes)) * age_whole_mean

        # drops the animes that were not reviewed (aka not recommended by others in the age range)
        age_anime_df.dropna(inplace=True)

        # getting the nth largest scores (high scored in that age range)
        age_animes_recommending = age_anime_df.nlargest(animes_to_recommend, 'weighted_score')
        age_recommendation = age_animes_recommending['title'].to_list()

        recommendations.append(["Recommendations based on your age", age_recommendation])
    if location is not None:
        # print('location recommending')
        if location.lower().strip() in location_user_df['country'].str.lower().values:
            # get only the users that are within the specifie country
            location_user = location_user_df[location_user_df['country'].str.lower().values == location.lower().strip()]

            # get only the user reviews that are within the specified country based off username
            location_anime_user_df = anime_user_df[anime_user_df['username'].isin(
                location_user['username'].to_list())]

            # according to IMDB top 250 formula
            # weighted rank = (v/(v+k))*X + (k/(v+k))*C
            # X = average for the movie(mean)
            # v = number of votes for the movie
            # k = minimum votes required to be listed in the top 250
            # C = the mean vote across the whole report
            location_whole_mean = anime_user_df['my_score'].mean()
            location_min_votes = 50
            location_anime_votes = location_anime_user_df.groupby('anime_id')['my_score'].agg('count')

            # make reading the graph and performing operations easier by grouping columns by username
            location_anime_user_df = location_anime_user_df.pivot(index='anime_id', columns='username',
                                                                  values='my_score')
            location_anime_mean = location_anime_user_df.mean(axis=1)

            # adds the IMDB top 250 formula to each of the animes and adds that as a new column
            location_anime_df = anime_df.copy(deep=True)
            location_anime_df['weighted_score'] = (location_anime_votes / (location_anime_votes + location_min_votes)) \
                                                  * location_anime_mean + (location_min_votes /
                                               (location_anime_votes + location_min_votes)) * location_whole_mean

            # drops the animes that were not reviewed (aka not recommended by others in the location)
            location_anime_df.dropna(inplace=True)

            location_animes_recommending = location_anime_df.nlargest(animes_to_recommend, 'weighted_score')
            location_recommendation = location_animes_recommending['title'].to_list()

            recommendations.append(["Recommendations based on your location", location_recommendation])

    # print('score recommending')
    score_animes_recommending = score_anime_df.nlargest(animes_to_recommend, 'score')
    score_recommendation = score_animes_recommending['title'].to_list()
    recommendations.append(["Highest scoring animes of all time", score_recommendation])

    # print('rank recommending')
    rank_animes_recommending = anime_df.nlargest(animes_to_recommend, 'rank')
    rank_recommendation = rank_animes_recommending['title'].to_list()
    recommendations.append(["Highest ranked animes of all time", rank_recommendation])

    if anime is not None:
        # print('rating recommending')
        # find the anime in our anime_df dataframe
        anime_in_data = anime_df[anime_df['title'] == anime]

        # if the anime exists in our data
        if len(anime_in_data):
            # rating recommendation
            # get the anime_id associated with the title
            rating_anime_id = anime_in_data['anime_id']._get_value(0, 'anime_id')

            # use KNN to find the animes that users recommend based on what users recommend this anime
            distances, indices = knn.kneighbors(csr_anime_user[rating_anime_id], n_neighbors=animes_to_recommend + 1)

            # sort the animes as tuples (index and distance)
            rating_recommended_animes_indices = sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())),
                                                key=lambda x: x[1])[:0:-1]
            rating_recommended_animes = []

            # grab the title of each anime and append to a list
            for index in rating_recommended_animes_indices:
                # print(index)
                recommended_anime_id = anime_user_df.iloc[index[0]]['anime_id']
                recommended_anime = anime_df[anime_df['anime_id'] == recommended_anime_id]['title'].values

                # we left out some data originally so this is to make sure that we don't recommend something that we cut out
                if len(recommended_anime):
                    if recommended_anime[0] != anime:
                        rating_recommended_animes.append(recommended_anime[0])

            recommendations.append(["Recommendations based on similar rated animes", rating_recommended_animes])

            # print('genre recommending')
            # genre recommendation
            # get the index of our anime
            genre_anime_id_idx = anime_df[anime_df['anime_id'] == int(anime_in_data['anime_id'])].index.values.astype(int)[0]

            # get the similarity scores of animes that are most like
            # the one we gave according to the cosine similarity
            sim_scores = list(enumerate(cos_sim[genre_anime_id_idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

            # omit the first anime because that is going to be the
            # same one that we inputted
            sim_scores = sim_scores[:animes_to_recommend + 1]
            sim_scores = sim_scores[1:]
            anime_indices = [idx[0] for idx in sim_scores]

            recommendations.append(["Recommendations based on similar genres", anime_df['title'].iloc[anime_indices].values])

    return recommendations


while True:
    print("Please enter your age, location, anime you want recommendations\n"
          "based off of, and how many you would like recommended.")
    print("{age},{location},{anime},{recommendations}")
    print("For values you don't want to fill in put 'na'")
    user_input = input()
    fields = user_input.split(',')

    user_age = None
    user_location = None
    user_anime = None
    user_recommendations = 10

    if fields[0].strip().lower() == "quit":
        break

    if fields[0] != 'na':
        user_age = int(fields[0])

    if fields[1] != 'na':
        user_location = fields[1]

    if fields[2] != 'na':
        user_anime = fields[2]

    if fields[3] != 'na':
        user_recommendations = int(fields[3])

    recs = get_recommendations(age=user_age, location=user_location,
                               anime=user_anime, animes_to_recommend=user_recommendations)

    for recommendation in recs:
        print(recommendation[0])

        for recc in recommendation[1]:
            print(recc)
