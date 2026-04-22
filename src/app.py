import streamlit as st
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

@st.cache_data
def cargar_datos():
    movies = pd.read_csv("data/movies.dat", sep="::", engine="python",
                         names=["movie_id", "title", "genres"], encoding="latin-1")
    ratings = pd.read_csv("data/ratings.dat", sep="::", engine="python",
                          names=["user_id", "movie_id", "rating", "timestamp"], encoding="latin-1")
    return movies, ratings

@st.cache_resource
def entrenar_modelo(ratings, movies):
    usuarios_activos = ratings.groupby("user_id")["rating"].count()
    usuarios_activos = usuarios_activos[usuarios_activos >= 50].index
    ratings_filtrado = ratings[ratings["user_id"].isin(usuarios_activos)]
    
    matriz = ratings_filtrado.pivot_table(index="user_id", columns="movie_id", values="rating")
    matriz_peliculas = csr_matrix(matriz.fillna(0).T.values)
    
    modelo = NearestNeighbors(metric="cosine", algorithm="brute", n_neighbors=10)
    modelo.fit(matriz_peliculas)
    
    return modelo, matriz

movies, ratings = cargar_datos()
modelo, matriz = entrenar_modelo(ratings, movies)

st.title("Recomendador de Peliculas")
st.markdown("Ingresa una película que te haya gustado y te recomendamos 5 similares.")

busqueda = st.text_input("Buscar película", placeholder="Ej: Matrix, Toy Story, Terminator...")

if busqueda:
    pelicula = movies[movies["title"].str.contains(busqueda, case=False, na=False)]
    
    if pelicula.empty:
        st.error(f"No se encontró ninguna película con '{busqueda}'")
    else:
        opciones = pelicula["title"].tolist()
        titulo_elegido = st.selectbox("¿Cuál de estas?", opciones)
        
        movie_id = movies[movies["title"] == titulo_elegido]["movie_id"].values[0]
        
        if movie_id not in matriz.columns:
            st.warning("Esta película no tiene suficientes ratings para recomendar.")
        else:
            idx = list(matriz.columns).index(movie_id)
            vector = csr_matrix(matriz.fillna(0).T.values)[idx]
            distancias, indices = modelo.kneighbors(vector, n_neighbors=6)
            
            st.subheader(f"Porque te gustó: {titulo_elegido}")
            st.write("Te recomendamos:")
            
            for i, idx_pelicula in enumerate(indices.flatten()[1:]):
                movie_id_rec = matriz.columns[idx_pelicula]
                titulo_rec = movies[movies["movie_id"] == movie_id_rec]["title"].values[0]
                generos = movies[movies["movie_id"] == movie_id_rec]["genres"].values[0]
                similitud = round((1 - distancias.flatten()[i+1]) * 100, 1)
                
                st.markdown(f"**{i+1}. {titulo_rec}**")
                st.caption(f"🎬 {generos} | Coincidencia: {similitud}%")