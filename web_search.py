import requests
from bs4 import BeautifulSoup
import webbrowser
from urllib.parse import urlparse
import json
from speak import speak
import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

search_history = []

def load_search_history():
    global search_history
    try:
        with open("search_history.json", "r") as file:
            search_history = json.load(file)
    except FileNotFoundError:
        search_history = []


def save_search_history():
    global search_history
    with open("search_history.json", "w") as file:
        json.dump(search_history, file, indent=4)


def google_search(query):
    formatted_query = query.replace(" ", "+")
    url = f"https://www.google.com/search?q={formatted_query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
    }

    # Send the request to Google
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        speak("Error retrieving search results.")
        print("Error retrieving search results.")
        return []

    # Parse the HTML
    soup = BeautifulSoup(response.text, "html.parser")
    search_results = []

    # Extract search results
    for item in soup.select("div.yuRUbf a"):
        if len(search_results) >= 10:
            break
        link = item["href"]
        domain = urlparse(link).netloc
        search_results.append((link, domain))

    return search_results

def add_search_to_history(chosen_link,domain,query):
    load_search_history()
# Add the selected link to search history
    search_history.append({
        "query": query,
        "link": chosen_link,
        "domain": domain,
        "timestamp": datetime.datetime.now().isoformat()
    })

    # Save the updated search history
    save_search_history()

def preprocess_queries(queries):
    clean_queries = []
    for query in queries:
        # Remove URLs
        query = re.sub(r"https?://\S+|www\.\S+", "", query)
        # Remove domain extensions
        query = re.sub(r"\b(?:com|org|net|edu|gov|io)\b", "", query)
        # Remove non-alphanumeric characters
        query = re.sub(r"[^a-zA-Z0-9\s]", "", query)
        # Convert to lowercase
        query = query.lower().strip()
        clean_queries.append(query)
    return clean_queries

def search(query):
    search_results = google_search(query)
    return search_results


def give_recommendations():
    load_search_history()

    raw_queries = [entry["query"] for entry in search_history]
    search_queries = preprocess_queries(raw_queries)
    visited_links = {entry["link"] for entry in search_history}

    # Use TF-IDF to find dominant topics in search history
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(search_queries)
    feature_names = vectorizer.get_feature_names_out()
    tfidf_scores = tfidf_matrix.sum(axis=0).A1
    top_indices = tfidf_scores.argsort()[-3:][::-1]  # Get top 3 features

    # Extract top topics
    top_topics = [feature_names[i] for i in top_indices]
    print(f"Top topics from your search history: {top_topics}")

    # Generate Google searches for the top topics
    recommendations = []
    for topic in top_topics:
        search_results = google_search(topic)
        for link, domain in search_results:
            if link not in visited_links:
                recommendations.append((topic, link,domain))

    return recommendations
