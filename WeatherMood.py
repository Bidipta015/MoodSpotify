import spotipy
import json
from spotipy.oauth2 import SpotifyClientCredentials


#
# def get_weather(city, api_key):
#     base_url = "https://api.openweathermap.org/data/2.5/weather"
#     params = {"q": city, "appid": api_key, "units": "metric"}
#     response = requests.get(base_url, params=params)
#     return response.json()

def weather_to_mood(weather):
    mood_map = {
        "Clear": "Happy",
        "Clouds": "Calm",
        "Rain": "Melancholy",
        "Drizzle": "Relaxing",
        "Snow": "Cozy",
        "Thunderstorm": "Intense",
    }
    return mood_map.get(weather, "Chill")


def get_songs(mood, client_id, client_secret):
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret))
    results = sp.search(q=f"mood:{mood}", type="track", limit=10)
    return results['tracks']['items']

def load_config(config_file):
    with open(config_file, "r") as file:
        return json.load(file)

if __name__ == '__main__':
    # Weather API and Spotify credentials
    config = load_config("config.json")
    spotify_client_id = config["SPOTIFY_CLIENT_ID"]
    spotify_client_secret = config["SPOTIFY_CLIENT_SECRET"]

    # Fetch weather data for a city
    #city = "London"
    #weather_data = get_weather(city, weather_api_key)

    # # Extract weather condition and map to mood
    # weather_condition = weather_data['weather'][0]['main']
    # mood = weather_to_mood(weather_condition)
    # print(f"The weather in {city} is '{weather_condition}', so the mood is '{mood}'.")

    # # Fetch songs based on mood
    # songs = get_songs(mood, spotify_client_id, spotify_client_secret)
    user_weather = input("How is the weather today (e.g., Clear, Clouds, Rain, Drizzle, Snow, Thunderstorm)? ").strip()
    mood = weather_to_mood(user_weather)
    print(f"The mood based on the weather is '{mood}'.")
    songs = get_songs(mood, spotify_client_id, spotify_client_secret)

    # Display recommended songs
    print("\nRecommended Songs:")
    for idx, song in enumerate(songs):
        print(f"{idx + 1}: {song['name']} by {song['artists'][0]['name']}")
