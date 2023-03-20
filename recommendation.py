from preprocessing import load_watched_animes
from sklearn.metrics.pairwise import cosine_similarity

def get_similar_animes (anime_id, animes, vectors, quantity = 10):
    try:
        anime_vector = vectors[animes[animes["anime_id"] == anime_id].index[0]]
        similarity_scores = cosine_similarity(anime_vector, vectors)
        similar_animes = [(animes.iloc[i]["anime_id"], similarity_scores[0][i]) for i in range(len(animes))]
        similar_animes.sort(key = lambda x: x[1], reverse = True)
        return similar_animes[:quantity]
    
    except:
        return list()

def get_unwatched_animes (user_watched, user_dropped, similar_animes):
    user_havent_watched = set()

    for anime_id in similar_animes:
        if anime_id not in [anime[0] for anime in user_watched] and anime_id not in [anime[0] for anime in user_dropped]:
            user_havent_watched.add(anime_id)

    return user_havent_watched

def get_user_favourites (watched_animes, quantity = 10):
    favourites = sorted(watched_animes.copy(), key = lambda anime: anime[1], reverse = True)[:quantity]
    return favourites

def get_recommendations (user, animes, vectors):
    response = load_watched_animes(user)
    
    if not response:
        return list()
    
    user_watched, user_dropped = response
    user_favourites = get_user_favourites(user_watched)

    similar_animes = set()

    for favourite_anime in user_favourites:
        similar_to_favourite = get_similar_animes(favourite_anime[0], animes, vectors)
        [similar_animes.add(anime[0]) for anime in similar_to_favourite]

    user_havent_watched = get_unwatched_animes(user_watched, user_dropped, similar_animes)
    
    recommendations = list()

    for anime_id in user_havent_watched:
        try:
            title, score = animes.loc[animes["anime_id"] == anime_id, ["title", "score"]].values.tolist()[0]

            if score >= 7.5:
                recommendations.append((title, score))
        
        except Exception:
            pass

    return [item[0] for item in sorted(recommendations, key = lambda anime: anime[1], reverse = True)]