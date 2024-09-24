from flask import Flask, request, render_template
import json
import requests
import pickle
import os
import io
import gdown
import random

app = Flask(__name__)

# Function to download a file from Google Drive
def download_file(url, output_path):
    gdown.download(url, output_path, quiet=False)

# Paths for the pickle files
artifacts_folder = 'artifacts'
if not os.path.exists(artifacts_folder):
    os.makedirs(artifacts_folder)

movie_list_path = os.path.join(artifacts_folder, 'movie_list.pkl')
similarity_path = os.path.join(artifacts_folder, 'similarity.pkl')

# URLs for the pickle files
url_movie_list = 'https://drive.google.com/uc?export=download&id=1bzmDYhHCOCI0dRLF72-6rt3DstLGbXT7'
url_similarity = 'https://drive.google.com/uc?id=1xrVHcbqtvdX5J435kvJ1FkQP8bT_Hj0e'

# Check if movie_list.pkl exists, if not, download it
if not os.path.exists(movie_list_path):
    print(f"{movie_list_path} not found. Downloading...")
    download_file(url_movie_list, movie_list_path)
else:
    print(f"{movie_list_path} found. No need to download.")

# Load movie_list
with open(movie_list_path, 'rb') as f:
    movie_list = pickle.load(f)

# Check if similarity.pkl exists, if not, download it
if not os.path.exists(similarity_path):
    print(f"{similarity_path} not found. Downloading...")
    download_file(url_similarity, similarity_path)
else:
    print(f"{similarity_path} found. No need to download.")

# Load similarity
with open(similarity_path, 'rb') as f:
    similarity = pickle.load(f)

print("Files checked, downloaded if necessary, and loaded successfully.")

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
api_keys = ['7058f3e1', '38bad860', 'fd237622', 'e189e68f', 'b4d0b532', '4bede092', 'a9e2d1c']

# Function to check which API key is valid (status code 200)
def check_api_key():
    test_movie = 'Inception'  # Using a test movie to check API key functionality
    for api_key in api_keys:
        url = f"http://www.omdbapi.com/?t={test_movie}&apikey={api_key}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                movie_data = response.json()
                # Ensure the API key returns valid movie data
                if 'Title' in movie_data:
                    print(f"Valid API key found: {api_key}")
                    return api_key
        except requests.exceptions.RequestException as e:
            print(f"Error with API key {api_key}: {e}")
    return None  # If no valid API key is found

api_key = check_api_key()

# Function to fetch movie details using the first valid API key
def movie_detail(movie_name):
    if api_key:
        url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                movie_data = response.json()
                if 'Title' in movie_data:
                    return movie_data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data with API key {api_key}: {e}")
    
    # Return default values if no valid response is obtained
    return {
        'Title': 'N/A',
        'Year': 'N/A',
        'Runtime': 'N/A',
        'imdbRating': 'N/A',
        'Poster': 'N/A'
    }

@app.route('/')
def home():
    movie_titles = movie_list['title'].to_list()
    first_four_movies = movie_titles[:4]
    home_movies = []
    for i in first_four_movies:
        movie_data = movie_detail(i)
        movie = {
            'title': movie_data['Title'],
            'year': movie_data['Year'],
            'runtime': movie_data['Runtime'],
            'imdbrating': movie_data['imdbRating'],
            'poster': movie_data['Poster']
        }
        home_movies.append(movie)
    return render_template('index.html', home_movies=home_movies)

# Route to display the home page with movie details
@app.route('/movie')
def movie():
    movie_name = request.args.get('movie_name')
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

if __name__ == "__main__":
    app.run()
