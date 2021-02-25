import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# read & import data into pandas data frame
anime_data = "anime.csv"
# set maximum number of rows to 20 & define NaN identifiers
pd.set_option('max_rows', 20)
idntfrs = ['na', '-', '--', '?', 'None', 'none', 'non', '', 'Not available', ' ']
anime_df = pd.read_csv(anime_data, na_values=idntfrs)

# discard unwanted items
anime_df.drop(['status', 'aired_string', 'score',
               'scored_by', 'members', 'popularity', 'rank'],
              axis=1, inplace=True)

# print(anime_df.head(3))

# separate the comma separated genres in the genre column
# and make each genre not case sensitive while also
# stripping away white space on the head/tail
anime_df['genre'] = anime_df['genre'].str.lower()
# print(anime_df.head(3))
anime_df['genre'] = anime_df['genre'].str.replace(',', '')
# print(anime_df.dtypes)
# print(anime_df.shape)
# print(anime_df[['anime_id', 'genre']].head(3))
# print(anime_df.head(3))

# initialize a count vectorizer to have a vocabulary
# of the many genres we are feeding into this algorithm
count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(anime_df['genre'])
# print(count_matrix.shape)

# use cosine similiarity to compare genres between animes
cos_sim = cosine_similarity(count_matrix, count_matrix)

def get_genre_based_recommendation(anime, cosine_sim=cos_sim, animes_to_recommend=10):
    # find the anime if it is in our dataset
    anime_in_data = anime_df[anime_df['title'] == anime]
    # print(anime_in_data)

    if len(anime_in_data):
        # print(anime_in_data['anime_id'])
        # get the index of our anime
        anime_id_idx = anime_df[anime_df['anime_id'] == int(anime_in_data['anime_id'])].index.values.astype(int)[0]
        # print(anime_id_idx)

        # get the similarity scores of animes that are most like
        # the one we gave according to the cosine similarity
        sim_scores = list(enumerate(cosine_sim[anime_id_idx]))
        # print(sim_scores)

        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # omit the first anime because that is going to be the
        # same one that we inputted
        sim_scores = sim_scores[:animes_to_recommend + 1]
        sim_scores = sim_scores[1:]
        # print(sim_scores)

        anime_indices = [idx[0] for idx in sim_scores]
        # print(anime_indices)

        return anime_df['title'].iloc[anime_indices]
    else:
        return "Try again with a different anime"


# Genre based collaborative filtering
print(get_genre_based_recommendation("Sword Art Online", animes_to_recommend=20))
