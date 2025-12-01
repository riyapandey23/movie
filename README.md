
---

## 🔁 How It Works (Step-by-step)

1. **Preprocessing & Model Building (Jupyter Notebook):**
   - Collect raw movie data (CSV / scraped / TMDB).
   - Clean and normalize fields (title, overview, genres, cast, keywords).
   - Vectorize textual fields (e.g., TF-IDF on overview + keywords; one-hot or count for genres/cast).
   - Combine feature vectors into a single matrix per movie.
   - Compute pairwise **cosine similarity** matrix and save to `similarity.pkl`.
   - Save movie list and metadata to `movies_list.pkl` / `movie_data.csv`.

2. **Backend (Flask / app.py):**
   - Load `movies_list.pkl` and `similarity.pkl` at startup.
   - Expose endpoint(s) to return recommendations for a given movie title/index.
   - Use OMDb API to fetch poster image URLs.
   - Use YouTube Data API to fetch trailer video IDs or embedded links.
   - Serve frontend templates and static assets.

3. **Frontend (HTML/CSS/JS):**
   - Dropdown for movie selection (populated from `movies_list`).
   - On selection, call Flask endpoint to get recommendations.
   - Render recommended movie cards (poster, title, overview, cast, release date, runtime, rating).
   - "Watch Trailer" button opens trailer view (embedded YouTube player).

---

## ⚙️ Setup & Run

1. **Clone repository**
```bash
git clone https://github.com/your-username/Movie-Recommender.git
cd Movie-Recommender
