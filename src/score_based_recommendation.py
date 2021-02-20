# import libraries
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

# read & import data into pandas data frame
anime_data = "anime.csv"

# set maximum number of rows to 20 & define NaN identifiers
pd.set_option('max_rows', 20)

anime_df = pd.read_csv(anime_data)

# get weighted score
anime_df["weighted_score"] = anime_df["score"] * anime_df["scored_by"] * 0.1

# print(anime_df.head())
# print(anime_df.nlargest(20, 'weighted_score'))

#Reducing sparsity using csr_matrix
csr_anime = csr_matrix((anime_df["weighted_score"], (anime_df.index, anime_df["anime_id"])))
# print(csr_anime)

# KNN with cosine distance metric
knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
knn.fit(csr_anime)


def get_score_based_recommendation(movie_name):
    animes_to_recommend = 10
    anime_in_data = anime_df[anime_df['title'].str.contains(movie_name, na=False)]
    # print(anime_in_data)
    if len(anime_in_data):
        anime_id = anime_in_data["anime_id"]

        distances, indices = knn.kneighbors(csr_anime[anime_id], n_neighbors=animes_to_recommend + 1)
        # print(distances)
        distances = distances[0]
        indices = indices[0]
        # print(indices)

        pairs = list(tuple(zip(indices, distances)))
        # print(pairs)

        recommended_animes = []

        for pair in pairs:
            possible_recommended_anime = anime_df.iloc[pair[0]]["title"]
            recommended_animes.append(possible_recommended_anime)

            # debug recommendation check
            # recommended_animes.append({'Title': anime_df.iloc[pair[0]]['title_english'], 'Distance': pair[1]})

        return recommended_animes
    else:
        return "No such anime in our records, please check again"


print(get_score_based_recommendation("Princess Tutu"))

