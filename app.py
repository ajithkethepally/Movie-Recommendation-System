import pickle
import streamlit as st
import requests
from PIL import Image


# Function to fetch movie poster
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id
    )
    data = requests.get(url)
    data = data.json()

    if "poster_path" in data:
        poster_path = data["poster_path"]
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        return None


# Function to recommend movies
def recommend(movie):
    index = movies[movies["title"] == movie].index
    if len(index) > 0:
        index = index[0]
        distances = sorted(
            list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1]
        )
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:6]:
            # Fetch the movie poster
            movie_id = movies.iloc[i[0]].movie_id
            poster = fetch_poster(movie_id)
            if poster:
                recommended_movie_posters.append(poster)
                recommended_movie_names.append(movies.iloc[i[0]].title)

        return recommended_movie_names, recommended_movie_posters
    else:
        return [], []


# Load movie data and similarity matrix
movies = pickle.load(open("model/movie_list.pkl", "rb"))
similarity = pickle.load(open("model/similarity.pkl", "rb"))

# Customizing the Streamlit app
st.set_page_config(page_title="CineGuru", page_icon="🎬", layout="wide")

# App header and sidebar
st.title("Movie Recommendation System")
st.sidebar.title("Options")
st.sidebar.markdown("Select a movie to get recommendations.")

# Movie selection dropdown with typeahead
selected_movie = st.sidebar.selectbox(
    "Choose a movie",
    movies["title"].unique(),
    index=0,
    format_func=lambda x: "Select a movie" if x == "" else x,
)

# Recommendation button
if st.sidebar.button("Get Recommendations"):
    if selected_movie != "Select a movie":
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

        if recommended_movie_names:
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                st.text(recommended_movie_names[0])
                st.image(recommended_movie_posters[0])

            with col2:
                st.text(recommended_movie_names[1])
                st.image(recommended_movie_posters[1])

            with col3:
                st.text(recommended_movie_names[2])
                st.image(recommended_movie_posters[2])

            with col4:
                st.text(recommended_movie_names[3])
                st.image(recommended_movie_posters[3])

            with col5:
                st.text(recommended_movie_names[4])
                st.image(recommended_movie_posters[4])

# Custom CSS styles
st.markdown(
    """
    <style>
    body {
        color: #333;
        background-color: #f9f9f9;
        font-family: Arial, sans-serif;
    }

    .streamlit-button {
        background-color: #F63366;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 0.75rem 1.25rem;
        border: none;
    }

    .streamlit-button:hover {
        background-color: #E81C61;
        cursor: pointer;
    }

    .streamlit-container {
        padding: 1rem;
    }

    .streamlit-header {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }

    .streamlit-sidebar .sidebar-content {
        background-color: #fff;
        padding: 1.5rem;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)
