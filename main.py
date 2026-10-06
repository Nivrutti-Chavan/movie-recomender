import streamlit as st
import pickle
import gzip

import pandas as pd
import requests

# =========================================================
# TMDB API KEY
# =========================================================

API_KEY ='b3055fb71521ac512aba662840dcb452'


# =========================================================
# LOAD MOVIE DATA
# =========================================================

with open("movie_dict.pkl", "rb") as file:
    movies_dict = pickle.load(file)

movies = pd.DataFrame(movies_dict)


# =========================================================
# LOAD SIMILARITY MATRIX
# =========================================================


with gzip.open("similarity.pkl.gz", "rb") as file:
    similarity = pickle.load(file)


# =========================================================
# FETCH POSTER FROM TMDB
# =========================================================

def fetch_poster(movie_title):

    url = "https://api.themoviedb.org/3/search/movie"

    params = {
        "api_key":'b3055fb71521ac512aba662840dcb452',
        "query": movie_title
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if data.get("results"):

            poster_path = data["results"][0].get("poster_path")

            if poster_path:

                poster_url = (
                    "https://image.tmdb.org/t/p/w500"
                    + poster_path
                )

                return poster_url

    except requests.exceptions.RequestException as e:

        print("TMDB Error:", e)

    return None


# =========================================================
# RECOMMENDATION FUNCTION
# =========================================================

def recommend(movie):

    movie_index = movies[movies["title"] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:

        movie_title = movies.iloc[i[0]]["title"]

        recommended_movies.append(movie_title)

        poster = fetch_poster(movie_title)

        recommended_posters.append(poster)

    return recommended_movies, recommended_posters


# =========================================================
# STREAMLIT UI
# =========================================================

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Movie Recommendation System")

st.write(
    "Select a movie and get 5 similar movie recommendations."
)


# =========================================================
# MOVIE DROPDOWN
# =========================================================

movie_list = list(movies["title"].values)

selected_movie = st.selectbox(
    "Select a movie",
    movie_list
)


# =========================================================
# RECOMMEND BUTTON
# =========================================================

if st.button("Recommend"):

    recommendations, posters = recommend(selected_movie)

    st.subheader("Recommended Movies")

    col1, col2, col3, col4, col5 = st.columns(5)

    columns = [
        col1,
        col2,
        col3,
        col4,
        col5
    ]

    for i in range(5):

        with columns[i]:

            if posters[i]:

                st.image(
                    posters[i],
                    use_container_width=True
                )

            else:

                st.write("Poster not available")

            st.write(
                f"**{recommendations[i]}**"
            )


# =========================================================
# TMDB CREDIT
# =========================================================

st.markdown("---")

st.caption(
    "This product uses the TMDB API but is not endorsed or certified by TMDB."
)

import gzip
import pickle

with gzip.open("similarity.pkl.gz", "rb") as f:
    similarity = pickle.load(f)


import os

TMDB_API_KEY = os.getenv("b3055fb71521ac512aba662840dcb452")