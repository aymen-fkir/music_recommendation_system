import pandas as pd

def favorite_genre(df : pd.DataFrame)->str:
    artist_genres = df["artist_genres"]
    genres = [gn for gens in artist_genres for gn in gens]
    counts_genres = [genres.count(gn) for gn in set(genres)]
    genres_unique = dict(zip(set(genres),counts_genres))
    favorite_genre = max(genres_unique, key=genres_unique.get)
    return favorite_genre





