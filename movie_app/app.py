import pandas as pd
import requests
from flask import Flask, render_template, request, redirect, url_for
import os
from dotenv import load_dotenv



app = Flask(__name__)

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
if not TMDB_API_KEY:
    raise ValueError("TMDB_API_KEY not found. Please check your .env file.")

BASE_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

# Load data
movies = pd.read_csv("data/movies.csv")

# Calculate weighted rating threshold and mean
m = movies["vote_count"].quantile(0.9)
C = movies["vote_average"].mean()

# Filter and compute scores
movies_filtered = movies.copy().loc[movies["vote_count"] > m]

def weighted_rating(df, m=m, C=C):
    R = df["vote_average"]
    v = df["vote_count"]
    return (v / (v + m)) * R + (m / (v + m)) * C

movies_filtered["score"] = movies_filtered.apply(weighted_rating, axis=1)
movies_sorted = movies_filtered.sort_values("score", ascending=False).head(100)

# Genre cache and TMDb metadata cache
genre_map = {}
cache = {}

def fetch_genres():
    global genre_map
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}&language=en-US"
    res = requests.get(url)
    genres = res.json().get("genres", [])
    genre_map = {g["id"]: g["name"] for g in genres}


def get_movie_metadata(title):
    if title in cache:
        return cache[title]

    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}"
    try:
        res = requests.get(url)
        data = res.json()
        if data['results']:
            movie = data['results'][0]
            metadata = {
                "id": movie.get("id"),
                "title": movie.get("title"),
                "overview": movie.get("overview"),
                "poster_url": BASE_IMAGE_URL + movie["poster_path"] if movie.get("poster_path") else None,
                "release_date": movie.get("release_date"),
                "vote_average": movie.get("vote_average"),
                "genre_ids": movie.get("genre_ids", [])
            }
            cache[title] = metadata
            return metadata
    except Exception as e:
        print(f"Error fetching metadata for {title}:", e)
    return None

@app.route("/")
def redirect_home():
    return redirect(url_for("home", page=1))

@app.route("/page/<int:page>")
def home(page):
    fetch_genres()
    query = request.args.get("q", "").lower()
    year_filter = request.args.get("year")
    genre_filter = request.args.get("genre")

    enriched_movies = []
    for _, row in movies_sorted.iterrows():
        metadata = get_movie_metadata(row['title'])
        if metadata:
            if query and query not in metadata['title'].lower():
                continue
            if year_filter and metadata['release_date'] and not metadata['release_date'].startswith(year_filter):
                continue
            if genre_filter:
                genre_names = [genre_map.get(gid) for gid in metadata['genre_ids']]
                if genre_filter not in genre_names:
                    continue
            enriched_movies.append(metadata)

    # Pagination
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(enriched_movies) + per_page - 1) // per_page
    page_movies = enriched_movies[start:end]

    # Get years and genres
    years = sorted({m['release_date'][:4] for m in cache.values() if m and m['release_date']})
    genres = sorted(set(g for movie in cache.values() for g in [genre_map.get(gid) for gid in movie['genre_ids']] if g))

    return render_template("index.html", movies=page_movies, years=years, genres=genres, page=page, total_pages=total_pages)

@app.route("/movie/<int:movie_id>")
def movie_detail(movie_id):
    for movie in cache.values():
        if movie and movie['id'] == movie_id:
            genre_names = [genre_map.get(gid) for gid in movie.get('genre_ids', []) if gid in genre_map]
            return render_template("movie.html", movie=movie, genres=genre_names)
    return "Movie not found", 404

if __name__ == "__main__":
    app.run(debug=True)
