import pickle
import requests
from flask import Flask, render_template, request, jsonify , redirect, url_for

app = Flask(__name__)
# API keys
OMDB_API_KEY = "3571f861"
YOUTUBE_API_KEY = "AIzaSyCfI8oEP-UMOO7-qv84w8tKlkkr1NgDEuE"

# Function to fetch movie details from OMDB
def fetch_movie_details(movie_title): 
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        trailer_url = get_youtube_trailer(movie_title)
        movie_details = {
            'title': data.get('Title', 'N/A'),
            'overview': data.get('Plot', 'N/A'),
            'genres': data.get('Genre', 'N/A'),
            'cast': data.get('Actors', 'N/A'),
            'release_date': data.get('Released', 'N/A'),
            'runtime': data.get('Runtime', 'N/A'),
            'vote_average': data.get('imdbRating', 'N/A'),
            'poster': data.get('Poster', 'https://via.placeholder.com/500'),
            'trailer': trailer_url
        }
        return movie_details
    else:
        return {}
# Function to get the trailer URL from YouTube
def get_youtube_trailer(movie_title):
    search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={movie_title} trailer&key={YOUTUBE_API_KEY}"
    response = requests.get(search_url)
    if response.status_code == 200:
        search_data = response.json()
        if 'items' in search_data and search_data['items']:
            video_id = search_data['items'][0]['id']['videoId']
            return f"https://www.youtube.com/embed/{video_id}"
    return None

# Function to fetch movie recommendations
def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movies = []
        for i in distances[1:6]:
            movie_title = movies.iloc[i[0]].title
            movie_details = fetch_movie_details(movie_title)
            recommended_movies.append(movie_details)
        return recommended_movies
    except Exception as e:
        print(f"Error fetching recommendations: {e}")
        return []

# Load movie data and similarity matrix
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('home.html', movie_list=movies['title'].values)

@app.route('/recommend', methods=['POST'])
def recommend_movies():
    movie = request.form['movie']
    recommendations = recommend(movie)
    return jsonify(recommendations)

@app.route('/movie/<title>')
def movie_details(title):
    details = fetch_movie_details(title)
    return render_template('movie_details.html', movie=details)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Add authentication logic here
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        feedback_text = request.form['feedback']
        # Process and store feedback here
        return redirect(url_for('home'))
    return render_template('feedback.html')

if __name__ == '__main__':
    app.run(debug=True)