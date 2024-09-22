# **Movie Recommendation System** 🎬  
An AI-based movie recommendation system that suggests movies based on content similarity and provides additional details like year, IMDb rating, runtime, and poster, utilizing the OMDb API. The project combines data pre-processing, machine learning, and web development, and has been deployed live using Flask on Render.

### **Live Link** 🔗
[Access the live app here](https://movie-recommandation-system-9njn.onrender.com/)

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

The files are retrieved from Google Drive in the Flask application using **`gdown`**.

---

## **Application Architecture**

1. **Frontend**: The web interface is developed using **HTML** and **Jinja templates** within Flask. Users can search for a movie, get recommendations, and view movie details.
2. **Backend**:
   - **Flask Application** serves as the backend where user requests are handled.
   - **Movie Recommendation Model**: The core recommendation engine is based on the content similarity model developed in the Jupyter Notebook.
   - **OMDb API Integration**: Movie details (such as runtime, IMDb rating, and poster) are fetched dynamically from the **OMDb API**.

---

## **Flask Integration & Deployment**

The **Flask** app (`app.py`) is designed to serve the recommendation model. It handles:
- Movie recommendations by computing cosine similarity.
- Fetching additional movie information using **OMDb API**.
  
### **Deployment**  
The Flask application is deployed on **Render**, making it accessible online. Render was chosen due to its free-tier services, ease of deployment, and ability to host Python-based web apps with minimal configuration.

**Deployed Link**: [Movie Recommendation App](https://movie-recommandation-system-9njn.onrender.com/)

---

## **API Usage & Key Management**

To fetch detailed information about the movies, such as IMDb rating, poster, and runtime, the app integrates with the **OMDb API**. Each API key has a daily request limit (1000 requests per day on the free tier).

### **Why Multiple API Keys?**  
Due to the limited number of daily requests allowed by the OMDb API, multiple API keys are managed in the application to avoid exceeding the daily quota. The keys are rotated, and their usage is tracked dynamically.

- **API Key Management**: 
   - The app tracks the usage count for each key and automatically switches to the next available key once the current one reaches its daily limit.
   - This ensures smooth functionality and prevents the system from being interrupted by key exhaustion.

---

## **Usage Instructions**

1. **Homepage**: Displays random movie recommendations with details such as title, year, runtime, IMDb rating, and poster.
2. **Search Functionality**: Users can search for a movie to get detailed information and 5 similar movies.
3. **Recommendation Engine**: Upon selecting a movie, the recommendation system suggests 5 movies with similar content.
4. **Movie Details**: The movie details, including IMDb rating and runtime, are fetched dynamically using the OMDb API.

---

## **Setup Guide**

Follow these steps to set up the project locally:

### **1. Clone the Repository**  
```bash
git clone https://github.com/your-username/movie-recommendation-system.git
cd movie-recommendation-system
```

### **2. Install the Required Libraries**  
Install the dependencies listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

### **3. Download the Pickle Files**  
Since the pickle files are too large for GitHub, they are hosted on Google Drive. The Flask app uses `gdown` to download them automatically, but you can manually download them using the following links:
- **Movie List**: [movie_list.pkl](https://drive.google.com/uc?export=download&id=1bzmDYhHCOCI0dRLF72-6rt3DstLGbXT7)
- **Similarity Matrix**: [similarity.pkl](https://drive.google.com/uc?export=download&id=1xrVHcbqtvdX5J435kvJ1FkQP8bT_Hj0e)

### **4. Run the Application**
Run the Flask application locally:
```bash
python app.py
```
Visit `http://127.0.0.1:5000/` in your browser to access the app.

---

## **Technologies Used**

- **Python**: Backend development, model training, and pre-processing.
- **Pandas** & **NumPy**: For data manipulation and processing.
- **Scikit-learn**: For vectorization and similarity computation.
- **Flask**: Web framework to serve the model.
- **HTML**, **CSS**, **Jinja**: For rendering the frontend.
- **OMDb API**: To fetch movie metadata.
- **Render**: For deploying the Flask application.

---

## **Future Enhancements**

- **Improved Search Functionality**: Implement a fuzzy search algorithm to handle partial or incorrect movie titles.
- **Real-time Movie Data**: Use live data from TMDB API for more up-to-date recommendations.
- **User Profiles**: Add a feature for users to create profiles and receive personalized recommendations based on their watch history.
- **Collaborative Filtering**: Expand the recommendation engine to include collaborative filtering techniques.

---