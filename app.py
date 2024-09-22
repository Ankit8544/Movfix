from flask import Flask, request, render_template
import json
import requests
import pickle
import os
import io
import gdown
import random

app = Flask(__name__)

# Download the file
url = 'https://drive.google.com/uc?export=download&id=1bzmDYhHCOCI0dRLF72-6rt3DstLGbXT7'
response = requests.get(url)

# Load the pickle file from the response content
if response.status_code == 200:
    movie_list = pickle.load(io.BytesIO(response.content))
else:
    print(f"Error downloading file: {response.status_code}")
    
# Download the file
url = 'https://drive.google.com/uc?id=1xrVHcbqtvdX5J435kvJ1FkQP8bT_Hj0e'

output = 'similarity.pkl'  # Temporary file to save the downloaded data
gdown.download(url, output, quiet=False)

# Load the pickle file
with open(output, 'rb') as f:
    similarity = pickle.load(f)

# Clean up if needed (remove the temporary file)
os.remove(output)

# Function to get movie recommendations
def recommend(movie):
    try:
        index = movie_list[movie_list['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movies = [movie_list.iloc[i[0]].title for i in distances[1:6]]
        return recommended_movies
    except IndexError:
        return ["Movie not found in the database."]

# Function to fetch movie details from the OMDB API
def movie_detail(movie_name):
    url = f"http://www.omdbapi.com/?t={movie_name}&apikey=7058f3e1"
    response = requests.get(url)
    movie_data = json.loads(response.text)
    return movie_data

@app.route('/')
def home():
    movie_titles = movie_list['title'].to_list()  # Assuming movie_list is a DataFrame or similar
    random_movies = random.sample(movie_titles, 4)

    home_movies = []

    for i in random_movies:
        # Fetch movie details only once to avoid multiple API calls
        movie_data = movie_detail(i)

        movie = {
            'title': movie_data.get('Title', 'Unknown Title'),
            'year': movie_data.get('Year', 'Unknown Year'),
            'runtime': movie_data.get('Runtime', 'Unknown Runtime'),
            'imdbrating': movie_data.get('imdbRating', 'N/A'),
            'poster': movie_data.get('Poster', '/path/to/default/poster.jpg')  # Use default poster if not available
        }
        home_movies.append(movie)

    return render_template('index.html', home_movies=home_movies)

# Route to display the home page with movie details
@app.route('/aaaa')
def aaaa():
    movie_name = request.args.get('movie_name', 'Avatar')
    # Get recommended movies list
    movie_suggestions_list = recommend(movie_name)
    movie_suggestions_list = movie_suggestions_list[:-1]
    movie_data = movie_detail(movie_name)
    movies_suggestions_data = []

    # Fetch details for each recommended movie
    for i in movie_suggestions_list:
        suggested_movie = movie_detail(i)
        movie = {
            'title': suggested_movie['Title'],
            'year': suggested_movie['Year'],
            'runtime': suggested_movie['Runtime'],
            'imdbrating': suggested_movie['imdbRating'],
            'poster': suggested_movie['Poster']
        }
        movies_suggestions_data.append(movie)

    return render_template('movie-details.html', movie_data=movie_data, suggested_movies=movies_suggestions_data)

if __name__ == '__main__':
    app.run(debug=True)
