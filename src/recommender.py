import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

def cargar_datos():
    movies = pd.read_csv("data/movies.dat", sep="::", engine="python",
                         names=["movie_id", "title", "genres"], encoding="latin-1")
    ratings = pd.read_csv("data/ratings.dat", sep="::", engine="python",
                          names=["user_id", "movie_id", "rating", "timestamp"], encoding="latin-1")
    return movies, ratings

def entrenar_modelo(ratings):
    usuarios_activos = ratings.groupby("user_id")["rating"].count()
    usuarios_activos = usuarios_activos[usuarios_activos >= 50].index
    ratings_filtrado = ratings[ratings["user_id"].isin(usuarios_activos)]
    matriz = ratings_filtrado.pivot_table(index="user_id", columns="movie_id", values="rating")
    matriz_peliculas = csr_matrix(matriz.fillna(0).T.values)
    modelo = NearestNeighbors(metric="cosine", algorithm="brute", n_neighbors=10)
    modelo.fit(matriz_peliculas)
    return modelo, matriz

def recomendar(titulo: str, movies, modelo, matriz) -> list:
    pelicula = movies[movies["title"].str.contains(titulo, case=False, na=False)]
    if pelicula.empty:
        return []
    movie_id = pelicula.iloc[0]["movie_id"]
    if movie_id not in matriz.columns:
        return []
    idx = list(matriz.columns).index(movie_id)
    vector = csr_matrix(matriz.fillna(0).T.values)[idx]
    distancias, indices = modelo.kneighbors(vector, n_neighbors=6)
    recomendaciones = []
    for i, idx_pelicula in enumerate(indices.flatten()[1:]):
        movie_id_rec = matriz.columns[idx_pelicula]
        titulo_rec = movies[movies["movie_id"] == movie_id_rec]["title"].values[0]
        generos = movies[movies["movie_id"] == movie_id_rec]["genres"].values[0]
        similitud = round((1 - distancias.flatten()[i+1]) * 100, 1)
        recomendaciones.append({
            "titulo": titulo_rec,
            "generos": generos,
            "similitud": similitud
        })
    return recomendaciones