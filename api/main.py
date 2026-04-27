from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.recommender import cargar_datos, entrenar_modelo, recomendar

app = FastAPI(title="Movie Recommender API")

# Carga el modelo una sola vez al iniciar
movies, ratings = cargar_datos()
modelo, matriz = entrenar_modelo(ratings)

class PeliculaRequest(BaseModel):
    pelicula: str

@app.get("/")
def root():
    return {"mensaje": "Movie Recommender API funcionando"}

@app.post("/recomendar")
def get_recomendaciones(request: PeliculaRequest):
    resultados = recomendar(request.pelicula, movies, modelo, matriz)
    if not resultados:
        raise HTTPException(status_code=404, detail=f"No se encontró '{request.pelicula}' o no tiene suficientes ratings")
    return {
        "pelicula": request.pelicula,
        "recomendaciones": resultados
    }

@app.get("/buscar/{titulo}")
def buscar_pelicula(titulo: str):
    resultados = movies[movies["title"].str.contains(titulo, case=False, na=False)]
    if resultados.empty:
        raise HTTPException(status_code=404, detail="No se encontraron películas")
    return {"peliculas": resultados["title"].tolist()[:10]}