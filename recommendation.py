from ast import literal_eval
from preprocessing import load_watched_animes

def compute_distances (user, user_watched, user_dropped, profiles):
    distances = list()

    for _, row in profiles.iterrows():
        neighbor = row["profile"]
        similarity = 0

        if neighbor != user:
            neighbor_favorites = [*map(int, literal_eval(row["favorites_anime"]))]
                
            for anime in neighbor_favorites:
                if anime in user_watched or anime in user_dropped:
                    similarity += 1
        
        distances.append((similarity, neighbor))
    
    distances.sort(reverse = True)
    return distances

def k_nearest_neighbors (user, user_watched, user_dropped, k, profiles):
    neighbors = compute_distances(user, user_watched, user_dropped, profiles)[:k]
    return neighbors

def get_unwatched_animes (user_watched, user_dropped, neighbors):
    user_havent_watched = set()

    for _, neighbor in neighbors:
        try:
            neighbor_watched, _ = load_watched_animes(neighbor)

            for anime in neighbor_watched:
                if anime not in user_watched and anime not in user_dropped:
                    user_havent_watched.add(anime)

        except Exception:
            pass

    return user_havent_watched

def get_recommendations (user, k, animes_data, profiles):
    response = load_watched_animes(user)
    
    if not response:
        return list()

    user_watched, user_dropped = response
    neighbors = k_nearest_neighbors(user, user_watched, user_dropped, k, profiles)
    user_havent_watched = get_unwatched_animes(user_watched, user_dropped, neighbors)
    
    recommendations = list()

    for anime in user_havent_watched:
        try:
            title, score = animes_data[anime]

            if score >= 8:
                recommendations.append((title, score))
        
        except Exception:
            pass

    return [item[0] for item in sorted(recommendations, key = lambda anime: anime[1], reverse = True)]