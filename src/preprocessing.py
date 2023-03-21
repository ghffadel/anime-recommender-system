from ast import literal_eval
from dotenv import load_dotenv
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from os import getenv
from scipy.sparse import hstack
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk, pandas as pd, requests

def prepare_nltk ():
    global stemmer, stop_words

    nltk.download("stopwords")
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words("english"))

def preprocess_synopsis (synopsis):
    try:
        global stemmer, stop_words

        synopsis = synopsis.lower().replace(",", "").replace(".", "").replace("(", "").replace(")", "").replace("-", " ")
        synopsis = " ".join([stemmer.stem(word) for word in synopsis.split() if word not in stop_words])

        return synopsis
    
    except:
        return ""

def preprocess_genre (genre):
    global stemmer, stop_words

    genre = list(set([item.lower() for item in literal_eval(genre)]))
    genre = " ".join([stemmer.stem(word) for word in genre if word not in stop_words])
    
    return genre

def load_animes ():
    df = pd.read_csv("animes.csv")
    df = df[["uid", "title", "synopsis", "genre", "score"]]
    df.rename(columns = {"uid": "anime_id"}, inplace = True)
    df = df.drop_duplicates()

    prepare_nltk()
    df["genre"] = df["genre"].apply(preprocess_genre)
    df["synopsis"] = df["synopsis"].apply(preprocess_synopsis)
    
    return df

def get_vectors (animes):
    genre_vectorizer = TfidfVectorizer()
    genre_vectors = genre_vectorizer.fit_transform(animes["genre"])

    synopsis_vectorizer = TfidfVectorizer()
    synopsis_vectors = synopsis_vectorizer.fit_transform(animes["synopsis"])

    combined_vectors = hstack((synopsis_vectors, genre_vectors))

    return combined_vectors

def get_api_key ():
    load_dotenv()
    return getenv("API_KEY")

def load_animes_from_api (user, status):
    try:
        response = requests.get(
            f"https://api.myanimelist.net/v2/users/{user}/animelist?fields=list_status&status={status}&limit=1000", 
            headers = { "X-MAL-CLIENT-ID": get_api_key() }
        )
        response = response.json()["data"]
        return response
    
    except Exception:
        return False

def load_watched_animes (user):
    animes, dropped = set(), set()

    for status in ["completed", "dropped", "on_hold", "watching"]:
        response = load_animes_from_api(user, status)

        if not response:
            continue

        for anime in response:
            if status == "dropped":
                dropped.add((anime["node"]["id"], anime["list_status"]["score"]))
            
            else:
                animes.add((anime["node"]["id"], anime["list_status"]["score"]))
    
    return (animes, dropped)

def get_animes_data (animes):
    animes_data = dict()

    for _, row in animes.iterrows():
        animes_data[row["anime_id"]] = (row["title"], float(row["score"]))

    return animes_data