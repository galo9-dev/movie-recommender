# Recomendador de Películas

Sistema de recomendación de películas basado en filtrado colaborativo usando el dataset MovieLens.

## Demo en vivo
https://movie-recommender-5hx9zqbd92yfvrysrxguxx.streamlit.app

## Qué hace
Ingresás una película que te gustó y el modelo te recomienda 5 películas similares basándose en los patrones de rating de miles de usuarios, sin usar géneros ni metadatos — solo comportamiento de usuarios.

## Tecnologías
- Python, Pandas, Scikit-learn, Scipy, Streamlit
- Algoritmo: KNN con similitud coseno

## Dataset
Se usó el dataset MovieLens con 1 millón de ratings de 6040 usuarios sobre 3883 películas. Los datos fueron recopilados entre 1997 y 2000, por lo que el catálogo incluye principalmente películas de los años 80 y 90. No es un modelo pensado para uso actual sino una demostración de cómo funciona el filtrado colaborativo con un volumen de datos representativo.

## Limitaciones
- El catálogo no incluye películas posteriores al año 2000
- Las recomendaciones se basan en patrones de usuarios de esa época

## Cómo correrlo localmente
1. Clonar el repo
2. Crear entorno virtual: `python -m venv venv`
3. Activar: `venv\Scripts\activate`
4. Instalar dependencias: `pip install -r requirements.txt`
5. Correr: `streamlit run src/app.py`