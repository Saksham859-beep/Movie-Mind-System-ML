import pickle
import streamlit as st
import requests

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}
.main {
    background-color: #0f2027;
}
h1 {
    text-align: center;
    color: #ffffff;
}
.movie-card {
    background-color: #1f2933;
    border-radius: 15px;
    padding: 10px;
    text-align: center;
    color: white;
    box-shadow: 0 10px 20px rgba(0,0,0,0.4);
}
.movie-title {
    font-weight: 600;
    font-size: 15px;
    margin-bottom: 8px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- FUNCTIONS ----------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"

    except requests.exceptions.RequestException:
        return "https://via.placeholder.com/500x750?text=Poster+Unavailable"


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    names = []
    posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        posters.append(fetch_poster(movie_id))
        names.append(movies.iloc[i[0]].title)

    return names, posters

# ---------------- HEADER ----------------
st.markdown("<h1>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#cbd5e1;'>Discover movies similar to your favorites</p>", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values

# ---------------- INPUT SECTION ----------------
st.markdown("### 🔍 Choose a Movie")
selected_movie = st.selectbox(
    "Start typing a movie name",
    movie_list
)

# ---------------- BUTTON ----------------
if st.button("✨ Recommend Movies"):
    with st.spinner("Finding the best movies for you..."):
        names, posters = recommend(selected_movie)

    st.markdown("### 🍿 Recommended Movies")

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.markdown(f"""
            <div class="movie-card">
                <div class="movie-title">{names[i]}</div>
            </div>
            """, unsafe_allow_html=True)
            st.image(posters[i], use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown("""
<hr style="border:1px solid #334155">
<p style="text-align:center;color:#94a3b8;">
Made with ❤️ using Machine Learning & Streamlit<br>
Dataset: TMDB
</p>
""", unsafe_allow_html=True)

