# 🎬 Movie Recommendation Web App

A Flask-based movie recommendation web app that uses weighted popularity scores and The Movie Database (TMDb) API to display top-rated movies, complete with poster images, overviews, filtering, search, pagination, and a dark-themed UI.

---

## 🚀 Features

- 🔍 Search for movies by title  
- 🎯 Filter movies by release year and genre  
- 📊 Rank movies using a weighted popularity formula (similar to IMDb)  
- 🖼️ Display metadata including posters, overviews, and ratings  
- 📄 Detail page for each movie with full info  
- 📃 Pagination for smoother browsing  
- 🌓 Dark-themed responsive card layout  
- 🔐 API key securely managed using `.env`

---

## 🛠 Tech Stack

- **Backend:** Python, Flask  
- **Frontend:** HTML, CSS (dark theme)  
- **Data:** Pandas, CSV, TMDb API  
- **Styling:** Custom CSS  
- **Environment:** Python virtual environment + dotenv

---

## 📦 Getting Started

### 📁 1. Clone the Repository

```bash
git clone https://github.com/Apoorva231/movie-recommendation-app.git
cd movie-recommendation-app
```

### 🧪 2. Set Up Virtual Environment

```bash
python -m venv venv
.\venv\Scripts\activate
```

### 📥 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If you don’t have a `requirements.txt` yet, generate one with:

```bash
pip freeze > requirements.txt
```

### 🔐 4. Create a `.env` File

In the root of the project, create a file named `.env` and add your TMDb API key like this:

```ini
TMDB_API_KEY=your_tmdb_api_key_here
```

### ▶️ 5. Run the App

```bash
cd movie_app
py app.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

---


Your TMDb API key from [TMDb](https://www.themoviedb.org/documentation/api) 

