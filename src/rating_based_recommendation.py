import pandas as pd
from scipy import sparse
from sklearn.neighbors import NearestNeighbors


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
# print(anime_df.head())
# print(anime_user_df.head())
# print(anime_user_df.shape)

# pivot the dataframe so that we can more easily extract user interpretations
anime_user_df = anime_user_df.pivot(index='anime_id', columns='username', values='my_score')

# Replacing all of the Nan value inputs with 0
anime_user_df.fillna(0, inplace=True)

# print(anime_user_df.head())
# print(anime_user_df.shape)

# Fills the dataframe into a csr_matrix so that we can
# remove sparsity from our data to make large
# computations faster
# csr_anime_user = csr_matrix(anime_user_df.values)

# reset the index so that we can search by index later
# when we want our recommendation
anime_user_df.reset_index(inplace=True)
# print(csr_anime_user)

# save our sparsity matrix so that we can access it later
# to save time
# sparse.save_npz("csr_anime_user.npz", csr_anime_user)
csr_anime_user = sparse.load_npz("csr_anime_user.npz")
# print(csr_anime_user)

# KNN to find similarities/trends among users
# Using cosine metric as well as brute force algorithm in the interest of time
knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
knn.fit(csr_anime_user)

# print(anime_df.head(10))


def get_rating_based_recommendation(anime, animes_to_recommend=10):
    # find the anime in our anime_df dataframe
    anime_in_data = anime_df[anime_df['title'] == anime]
    # print(anime_in_data)

    # if the anime exists in our data
    if len(anime_in_data):
        # get the anime_id associated with the title
        anime_id = anime_in_data['anime_id']._get_value(0, 'anime_id')

        # get the index of the anime in our user dataframe
        anime_id_idx = anime_user_df[anime_user_df['anime_id'] == anime_id]
        # print(anime_id_idx)

        # print(anime_id)
        # print(csr_anime_user[anime_id])

        # use KNN to find the animes that users recommend based on what users recommend this anime
        distances, indices = knn.kneighbors(csr_anime_user[anime_id], n_neighbors=animes_to_recommend+1)
        # print(indices)
        # sort the animes as tuples (index and distance)
        recommended_animes_indices = sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())), key=lambda x: x[1])[:0:-1]
        recommended_animes = []
        # print(recommended_animes_indices)

        #grab the title of each anime and append to a list
        for index in recommended_animes_indices:
            # print(index)
            recommended_anime_id = anime_user_df.iloc[index[0]]['anime_id']
            recommended_anime = anime_df[anime_df['anime_id'] == recommended_anime_id]['title'].values

            # we left out some data originally so this is to make sure that we don't recommend something that we cut out
            if len(recommended_anime):
                recommended_animes.append(recommended_anime[0])

        return recommended_animes
    else:
        return "No found anime. Try again"


# User based collaborative filtering
print(get_rating_based_recommendation("Sword Art Online", animes_to_recommend=15))
