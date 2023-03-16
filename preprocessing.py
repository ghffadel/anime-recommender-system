from dotenv import load_dotenv
from os import getenv
import pandas as pd, requests

def load_animes ():
    df = pd.read_csv("animes.csv")
    df = df[['uid', 'title', 'genre', 'members', 'popularity', 'ranked', 'score']]
    df.rename(columns = {'uid': 'anime_id'}, inplace = True)
    df = df.drop_duplicates()
    return df

def load_profiles ():
    df = pd.read_csv("profiles.csv")
    df = df[['profile', 'favorites_anime']]
    df = df.drop_duplicates()
    return df

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
                dropped.add(anime["node"]["id"])
            
            else:
                animes.add(anime["node"]["id"])
    
    return (animes, dropped)

def get_animes_data (animes):
    animes_data = dict()

    for _, row in animes.iterrows():
        animes_data[row["anime_id"]] = (row["title"], float(row["score"]))

    return animes_data