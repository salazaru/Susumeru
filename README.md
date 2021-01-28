# weebythingsfornonweebs
Interpretable Anime Recommendation System &amp; Trend Analyzer

Interpretable Anime Recommender & Trend Analyzer

Our recommender system has two approaches: by analyzing the correlation between the user and the anime, and by analyzing the correlation between one anime and another.
To obtain the correlation between one anime and another we could first extract the features of the anime series using principle component analysis(PCA) for features like genre, producer, rating. Then, we use unsupervised learning like K-means to cluster the anime series with similar features. This way, for a given anime series, we could recommend similar anime series.
To analyze the between the user and the anime, we could extract and analyze(taking average or split into clusters) the features of the anime series the user viewed, and recommend animes with similar features.

Due to the interpretability of our recommender system, it can be used by consumers to find the best anime to watch according to their tastes. Further, the analysis of trends may inform anime producers and distributors as to where the industry is heading.

