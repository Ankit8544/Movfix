# **Movie Recommendation System** 🎬  
An Content based movie recommendation system that suggests movies based on content similarity and provides additional details like year, IMDb rating, runtime, and poster, utilizing the OMDb API. The project combines data pre-processing, machine learning, and web development, and has been deployed live using Flask.

### **Live Link** 🔗
[Access the live app here](https://movfix.onrender.com)

---

## **Table of Contents**
- [Project Overview](#project-overview)
- [Data Preprocessing & Model Training](#data-preprocessing--model-training)
- [Application Architecture](#application-architecture)
- [Flask Integration & Deployment](#flask-integration--deployment)
- [API Usage & Key Management](#api-usage--key-management)
- [Usage Instructions](#usage-instructions)
- [Setup Guide](#setup-guide)
- [Technologies Used](#technologies-used)
- [Future Enhancements](#future-enhancements)

---

## **Project Overview**

This project is a **Content-Based Movie Recommendation System** that recommends movies based on the similarity of genres, keywords, cast, and crew members. The core model is developed in a Jupyter Notebook (`Movie.ipynb`), where we preprocess movie data from **TMDB (The Movie Database)** and compute the content similarity between different movies using **Cosine Similarity** on the preprocessed features.

To make the system interactive, we built a Flask web application, which serves the trained model and provides users with movie recommendations. Additional movie information is fetched from the **OMDb API** and displayed on the UI.

---

## **Data Preprocessing & Model Training**

### **Data Source**  
The datasets used in this project are:
- **`tmdb_5000_movies.csv`**: Contains movie metadata such as genres, keywords, overview, etc.
- **`tmdb_5000_credits.csv`**: Includes cast and crew details for each movie.

### **Preprocessing Pipeline**
In the **`Movie.ipynb`** file, the following steps were performed:

1. **Data Cleaning**: Dropped missing or irrelevant columns and handled duplicates.
2. **Feature Engineering**:
   - Extracted and converted `genres`, `keywords`, `cast`, and `crew` columns from stringified lists to actual lists.
   - Selected only the top 3 cast members and fetched the director for each movie.
   - Converted text in the `overview` column to word tokens.
3. **Stemming**: Applied **Porter Stemming** to normalize the text.
4. **Vectorization**: Used **CountVectorizer** to convert textual data into vectors with a max feature limit of 5000.
5. **Similarity Calculation**: Computed pairwise **cosine similarity** to create the recommendation engine.

### **Model Storage**  
Given the large size of the trained model and data, it was saved as a **pickle file**. Due to GitHub limitations, the pickle files were uploaded to **Google Drive** for efficient storage and retrieval:
- **`movie_list.pkl`**: Contains the preprocessed movie data.
- **`similarity.pkl`**: Contains the cosine similarity matrix.

---

## **Application Architecture**

The application consists of two main components:

1. **Backend**:  
   The backend is built using **Flask**, which handles the model predictions and serves movie recommendations. The pre-trained recommendation model, stored as a pickle file, is loaded into the application when it starts. The backend also communicates with the OMDb API to fetch additional movie details.

2. **Frontend**:  
   The frontend is rendered using **HTML** and **CSS** templates in Flask. It displays recommended movie results, details about the movies like IMDb rating, runtime, year, and posters fetched from OMDb.

---

## **Flask Integration & Deployment**

### **Flask Setup**
The Flask web app serves the trained model and handles API requests to OMDb. It has two main routes:

- `/`: Displays four movies on the homepage with details like the title, year, runtime, IMDb rating, and poster.
- `/movie`: Takes the movie name as input, recommends similar movies, and fetches their details from OMDb.

### **Deployment**
The application is deployed live on **Render**. Flask handles routing, fetching recommendations, and integrating OMDb movie details.

---

## **API Usage & Key Management**

We use the **OMDb API** to retrieve detailed information about movies, such as the IMDb rating, year of release, runtime, and poster. To avoid reaching API limits, we rotate between multiple API keys.

### **API Keys**
A list of API keys is maintained in the `app.py` file. The application checks which API key is valid by testing a request to fetch the movie 'Inception'. If the key returns valid data, it is used for all subsequent API requests. If the key fails, the next one in the list is tested.

---

## **Usage Instructions**

1. **Homepage**:  
   - When you visit the homepage, you'll see a few popular movies with their details like the title, IMDb rating, year, runtime, and poster.
   
2. **Search Functionality**:  
   - You can search for any movie title on the website, and the system will suggest similar movies based on content similarity.
   
3. **Movie Details**:  
   - For each recommended movie, the app fetches details such as IMDb rating, year, runtime, and poster using the OMDb API.

---

## **Setup Guide**

### **Requirements**
- Python 3.x
- Flask
- Pandas, NumPy, Scikit-learn
- CountVectorizer (from sklearn)
- Requests library
- Pickle library
- OMDb API keys (free keys can be generated from the [OMDb website](http://www.omdbapi.com/apikey.aspx))

### **Steps to Run Locally**

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/movie-recommendation-system.git
   cd movie-recommendation-system
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download the **pickle** files (movie list and similarity matrix):
   - **movie_list.pkl**: [Download Link](https://drive.google.com/file/d/1bzmDYhHCOCI0dRLF72-6rt3DstLGbXT7/view)
   - **similarity.pkl**: [Download Link](https://drive.google.com/file/d/1xrVHcbqtvdX5J435kvJ1FkQP8bT_Hj0e/view)
   
   Save these files to the `artifacts/` folder in your project directory.

4. Run the Flask app:
   ```bash
   python app.py
   ```

5. Visit the app in your browser at `http://127.0.0.1:5000`.

---

## **Technologies Used**

- **Python**: For data preprocessing, model building, and backend logic.
- **Flask**: To build and serve the web application.
- **Pandas & NumPy**: For data manipulation and processing.
- **Scikit-learn**: To perform vectorization and calculate content similarity.
- **OMDb API**: For fetching movie details.
- **HTML, CSS**: For creating the user interface.
- **Google Drive & gdown**: To store and retrieve model files.

---

## **Future Enhancements**

1. **Collaborative Filtering**: Implementing collaborative filtering to complement the content-based approach, providing recommendations based on user ratings.
   
2. **Improved Movie Search**: Adding autocomplete functionality in the search bar for better user experience.

3. **Real-time Movie Database**: Updating the dataset to include the latest movie releases, leveraging an external movie database API.

4. **UI Enhancements**: Improving the UI to make it more user-friendly and visually appealing with dynamic features.

---
