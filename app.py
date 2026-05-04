import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

:root {
    --bg: #0a0a0f;
    --surface: #12121a;
    --surface2: #1a1a26;
    --accent: #e8c547;
    --accent2: #ff6b35;
    --text: #f0f0f0;
    --muted: #8888aa;
    --border: #2a2a3a;
}

html, body, [class*="css"] {
    background-color: var(--bg);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}
.stApp { background: var(--bg); }
.block-container { padding: 2rem 3rem 4rem; max-width: 1100px; }
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

.hero {
    text-align: center;
    padding: 3.5rem 0 2rem;
}
.hero-eyebrow {
    font-family: 'DM Sans', sans-serif;
    font-weight: 300;
    font-size: 0.8rem;
    letter-spacing: 0.4em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(4rem, 10vw, 7rem);
    line-height: 0.9;
    letter-spacing: 0.04em;
    color: var(--text);
    margin: 0;
}
.hero-title span { color: var(--accent); }
.hero-sub {
    font-size: 1rem;
    color: var(--muted);
    margin-top: 1rem;
    font-weight: 300;
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 2rem 0;
}

.stats-row {
    display: flex;
    gap: 1rem;
    margin: 1.5rem 0;
}
.stat-chip {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 0.5rem 1rem;
    font-size: 0.8rem;
    color: var(--muted);
    flex: 1;
    text-align: center;
}
.stat-chip strong {
    display: block;
    font-size: 1.1rem;
    color: var(--accent);
    font-family: 'Bebas Neue', sans-serif;
    letter-spacing: 0.05em;
}

div[data-testid="stNumberInput"] input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1.1rem !important;
    padding: 0.6rem 1rem !important;
}
div[data-testid="stNumberInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(232,197,71,0.15) !important;
}

div.stButton > button {
    background: var(--accent) !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.1rem !important;
    letter-spacing: 0.1em !important;
    padding: 0.6rem 2.5rem !important;
    width: 100%;
    transition: all 0.2s ease !important;
}
div.stButton > button:hover {
    background: #f5d76e !important;
    transform: translateY(-1px);
}

.input-label {
    font-size: 0.72rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.4rem;
}

.section-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    letter-spacing: 0.1em;
    color: var(--text);
    margin: 2rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.movie-grid { display: flex; flex-direction: column; gap: 0.6rem; }
.movie-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 1rem 1.25rem;
    display: flex;
    align-items: center;
    gap: 1.25rem;
    transition: border-color 0.2s, background 0.2s;
    position: relative;
    overflow: hidden;
}
.movie-card:hover {
    border-color: var(--accent);
    background: var(--surface2);
}
.movie-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: var(--accent);
    opacity: 0;
    transition: opacity 0.2s;
}
.movie-card:hover::before { opacity: 1; }
.card-rank {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem;
    color: var(--border);
    min-width: 2.5rem;
    text-align: center;
    line-height: 1;
}
.card-info { flex: 1; min-width: 0; }
.card-title {
    font-size: 0.95rem;
    font-weight: 500;
    color: var(--text);
    margin-bottom: 0.3rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.genre-tag {
    display: inline-block;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: 3px;
    padding: 0.1rem 0.4rem;
    margin-right: 0.3rem;
    font-size: 0.65rem;
    color: var(--muted);
}
.card-rating { text-align: right; min-width: 5rem; }
.rating-score {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    line-height: 1;
    color: var(--accent);
}
.rating-stars { font-size: 0.65rem; color: var(--muted); }

.history-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 0.75rem 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.4rem;
}
.history-title { font-size: 0.85rem; color: var(--text); }
.history-rating {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.1rem;
    color: var(--accent2);
    white-space: nowrap;
    margin-left: 0.5rem;
}

.app-footer {
    text-align: center;
    padding: 2rem 0 0;
    font-size: 0.72rem;
    color: var(--border);
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)


# ─── Load Data & Model ─────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    base = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(base, "svd_model.pkl"), "rb") as f:
        return pickle.load(f)

@st.cache_data
def load_data():
    base = os.path.dirname(os.path.abspath(__file__))
    movies = pd.read_csv(os.path.join(base, "movies_data.csv"))
    ratings = pd.read_csv(os.path.join(base, "ratings_data.csv"))
    return movies, ratings

model = load_model()
movies, ratings = load_data()

def rating_to_stars(r):
    full = int(r)
    half = 1 if (r % 1) >= 0.5 else 0
    empty = 5 - full - half
    return "★" * full + "½" * half + "☆" * empty

def get_recommendations(user_id, n=10):
    rated = set(ratings[ratings["userId"] == user_id]["movieId"])
    unrated = movies[~movies["movieId"].isin(rated)]["movieId"].tolist()
    preds = [(mid, model.predict(user_id, mid).est) for mid in unrated]
    preds.sort(key=lambda x: x[1], reverse=True)
    results = []
    for i, (mid, est) in enumerate(preds[:n]):
        info = movies[movies["movieId"] == mid].iloc[0]
        results.append({
            "rank": i + 1,
            "title": info["title"],
            "genres": info["genres"],
            "predicted_rating": round(est, 2),
        })
    return pd.DataFrame(results)

def get_user_history(user_id, n=5):
    user_r = ratings[ratings["userId"] == user_id].sort_values("rating", ascending=False).head(n)
    return user_r.merge(movies, on="movieId")[["title", "rating"]]


# ─── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <p class="hero-eyebrow">SVD · Collaborative Filtering · MovieLens</p>
    <h1 class="hero-title">CINE<span>MATCH</span></h1>
    <p class="hero-sub">Film recommendation system powered by Singular Value Decomposition</p>
</div>
""", unsafe_allow_html=True)

total_users = ratings["userId"].nunique()
total_movies = movies["movieId"].nunique()
total_ratings = len(ratings)
sparsity = 1 - (total_ratings / (total_users * total_movies))

st.markdown(f"""
<div class="stats-row">
    <div class="stat-chip"><strong>{total_users}</strong>Users</div>
    <div class="stat-chip"><strong>{total_movies:,}</strong>Films</div>
    <div class="stat-chip"><strong>{total_ratings:,}</strong>Ratings</div>
    <div class="stat-chip"><strong>0.879</strong>RMSE</div>
    <div class="stat-chip"><strong>{sparsity*100:.1f}%</strong>Sparsity</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ─── Input ─────────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([3, 1])
with col_input:
    st.markdown('<p class="input-label">User ID (1 – 610)</p>', unsafe_allow_html=True)
    user_id = st.number_input("uid", min_value=1, max_value=610, value=1, step=1, label_visibility="collapsed")
with col_btn:
    st.markdown('<p class="input-label">&nbsp;</p>', unsafe_allow_html=True)
    search = st.button("GET RECOMMENDATIONS")

# ─── Results ───────────────────────────────────────────────────────────────────
if search:
    valid_users = set(ratings["userId"].unique())
    if user_id not in valid_users:
        st.warning(f"User ID {user_id} tidak ditemukan dalam dataset.")
    else:
        with st.spinner("Menghitung rekomendasi..."):
            recs = get_recommendations(user_id, n=10)
            history = get_user_history(user_id, n=5)

        col_rec, col_hist = st.columns([3, 2], gap="large")

        with col_rec:
            st.markdown('<div class="section-title">🎬 Top 10 Rekomendasi</div>', unsafe_allow_html=True)
            st.markdown('<div class="movie-grid">', unsafe_allow_html=True)
            for _, row in recs.iterrows():
                genres_html = "".join(
                    f'<span class="genre-tag">{g}</span>'
                    for g in str(row["genres"]).split("|")[:3]
                )
                stars = rating_to_stars(row["predicted_rating"])
                st.markdown(f"""
                <div class="movie-card">
                    <div class="card-rank">{row['rank']:02d}</div>
                    <div class="card-info">
                        <div class="card-title">{row['title']}</div>
                        <div>{genres_html}</div>
                    </div>
                    <div class="card-rating">
                        <div class="rating-score">{row['predicted_rating']}</div>
                        <div class="rating-stars">{stars}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_hist:
            n_rated = len(ratings[ratings["userId"] == user_id])
            avg_r = ratings[ratings["userId"] == user_id]["rating"].mean()
            st.markdown(f'<div class="section-title">👤 Profil User {user_id}</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="stats-row" style="margin:0 0 1.25rem">
                <div class="stat-chip"><strong>{n_rated}</strong>Film Dirating</div>
                <div class="stat-chip"><strong>{avg_r:.2f}</strong>Avg Rating</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('<p class="input-label" style="margin-bottom:.5rem">Rating tertinggi user ini</p>', unsafe_allow_html=True)
            for _, row in history.iterrows():
                title = row['title']
                short = title[:40] + "…" if len(title) > 40 else title
                st.markdown(f"""
                <div class="history-card">
                    <div class="history-title">{short}</div>
                    <div class="history-rating">★ {row['rating']}</div>
                </div>
                """, unsafe_allow_html=True)

st.markdown('<div class="divider" style="margin-top:3rem"></div>', unsafe_allow_html=True)
st.markdown("""
<div class="app-footer">
    CineMatch · SVD Collaborative Filtering · MovieLens Latest Small · Capstone Project
</div>
""", unsafe_allow_html=True)
