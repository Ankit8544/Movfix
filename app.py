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
output = 'movie_list.pkl'
gdown.download(url, output, quiet=False)
with open(output, 'rb') as f:
    movie_list = pickle.load(f)
os.remove(output)
   
# Download the similarity pickel file
url = 'https://drive.google.com/uc?id=1xrVHcbqtvdX5J435kvJ1FkQP8bT_Hj0e'
output = 'similarity.pkl'
gdown.download(url, output, quiet=False)
with open(output, 'rb') as f:
    similarity = pickle.load(f)
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
api_keys = ['7058f3e1', '38bad860', 'fd237622', 'e189e68f']  # Add more keys as needed
api_key_usage = {key: 0 for key in api_keys}  # Dictionary to track API key usage
request_limit = 1000  # Set to OMDb's free daily limit

# Function to fetch movie details from the OMDB API using multiple keys
def movie_detail(movie_name):
    global api_keys, api_key_usage
    # Loop through each API key until one works or limit is hit
    for api_key in api_keys:
        # Check if the current API key has reached its limit
        if api_key_usage[api_key] < request_limit:
            url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
            response = requests.get(url)
            movie_data = json.loads(response.text)

            # Increment the usage count for the current API key
            api_key_usage[api_key] += 1

            # Check if the response contains the 'Title' key (indicating success)
            if 'Title' in movie_data:
                return movie_data

    # If no keys worked or all hit the limit, return default values
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
    random_movies = random.sample(movie_titles, 4)
    home_movies = []
    for i in random_movies:
        movie = {
            'title': movie_detail(i)['Title'],
            'year': movie_detail(i)['Year'],
            'runtime': movie_detail(i)['Runtime'],
            'imdbrating': movie_detail(i)['imdbRating'],
            'poster': movie_detail(i)['Poster']
        }
        home_movies.append(movie)
    return render_template('index.html', home_movies=home_movies)

# Route to display the home page with movie details
@app.route('/movie')
def movie():
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

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
