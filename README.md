# weebythingsfornonweebs

Interpretable Anime Recommender & Trend Analyzer

Our recommender system has two approaches: by analyzing the correlation between the user and the anime, and by analyzing the correlation between one anime and another. To obtain the correlation between one anime and another we could first extract the features of the anime series using principal component analysis (PCA) for features like genre, producer, and rating. Next, we will use unsupervised learning like K-means to cluster the anime series with similar features. This way, for a given anime series, we could recommend similar anime series. To analyze the ranking between the user and the anime, we could extract and analyze (taking average or split into clusters) the features of the anime series the user viewed and recommend animes with similar features. Due to the interpretability of our recommender system, it can be used by consumers to find the best anime to watch according to their tastes. Further, the analysis of trends may inform anime producers and distributors as to where the industry is heading.

## Broad trends to analyze:
1. Genre evolution over time.
2. Genre vs gender with a selector for age range.
3. How are genres clustered? Does one genre necessarily imply another?

## User trends to analyze:
1. Where do certain people watch titles from? Is there a correlation? Popularity by location?
2. Viewer ages.
3. We can use the dates when an anime is watched by a user to gauge if it is still relevant after it has aired. Just a plot of when people are watching.
