import spotipy
from datetime import datetime
from spotipy.oauth2 import SpotifyClientCredentials
import json


def load_config(config_file):
    """
    Loads configuration data from a JSON file.
    """
    with open(config_file, "r") as file:
        return json.load(file)


def get_cycle_phase(period_date):
    """
    Determines the phase of the menstrual cycle based on the start date of the last period.
    """
    today = datetime.now()
    cycle_day = (today - period_date).days % 28  # Assumes a 28-day cycle

    if 1 <= cycle_day <= 5:
        return "Menstrual"
    elif 6 <= cycle_day <= 13:
        return "Follicular"
    elif 14 <= cycle_day <= 16:
        return "Ovulation"
    elif 17 <= cycle_day <= 28:
        return "Luteal"
    else:
        return "Unknown"


def phase_to_mood(phase):
    """
    Maps menstrual cycle phases to moods.
    """
    phase_mood_map = {
        "Menstrual": "Relaxing",
        "Follicular": "Happy",
        "Ovulation": "Romantic",
        "Luteal": "Melancholy"
    }
    return phase_mood_map.get(phase, "Chill")


def get_songs(mood, client_id, client_secret, language=None, era=None, genre=None, artist=None):
    """
    Fetches songs from Spotify based on the given mood and user preferences.
    """
    try:
        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(
            client_id=client_id, client_secret=client_secret))
    except Exception as e:
        raise RuntimeError(f"Spotify client initialization failed: {e}")

    # Build dynamic query
    query = f"mood:{mood}"
    if language:
        query += f" language:{language}"
    if era:
        query += f" year:{era}"
    if genre:
        query += f" genre:{genre}"
    if artist:
        query += f" artist:{artist}"

    try:
        results = sp.search(q=query, type="track", limit=10)
        return results['tracks']['items']
    except Exception as e:
        raise RuntimeError(f"Spotify search query failed: {e}")


if __name__ == '__main__':
    try:
        # Load Spotify credentials from config.json
        config = load_config("config.json")
        spotify_client_id = config.get("SPOTIFY_CLIENT_ID")
        spotify_client_secret = config.get("SPOTIFY_CLIENT_SECRET")

        if not spotify_client_id or not spotify_client_secret:
            raise ValueError("Spotify Client ID or Secret is missing in config.json")

        # Ask the user for the last period date
        input_date = input("Enter the date of your last period (DD) from last month: ").strip()
        current_year = datetime.now().year
        current_month = datetime.now().month

        # Adjust the year and month to last month
        last_month = current_month - 1 if current_month > 1 else 12
        year_adjustment = current_year - 1 if current_month == 1 else current_year

        # Construct the full date for the last period
        period_date = datetime.strptime(f"{year_adjustment}-{last_month}-{input_date}", "%Y-%m-%d")

        # Determine cycle phase and corresponding mood
        phase = get_cycle_phase(period_date)
        mood = phase_to_mood(phase)
        print(f"Your current cycle phase is '{phase}', so the mood is '{mood}'.")

        # Ask for user preferences
        language = input("Enter preferred language (e.g., English, Spanish, leave blank for any): ").strip() or None
        era = input(
            "Enter preferred era (e.g., pre-2000 for retro, 2000-2024 for current, leave blank for any): ").strip() or None
        genre = input("Enter preferred genre (e.g., Pop, Rock, leave blank for any): ").strip() or None
        artist = input("Enter preferred artist (leave blank for any): ").strip() or None

        # Fetch songs based on mood and preferences
        songs = get_songs(mood, spotify_client_id, spotify_client_secret, language, era, genre, artist)

        # Display recommended songs
        print("\nRecommended Songs:")
        if songs:
            for idx, song in enumerate(songs):
                print(f"{idx + 1}: {song['name']} by {song['artists'][0]['name']}")
        else:
            print("No songs found based on your preferences.")

    except ValueError as ve:
        print(f"Input Error: {ve}")
    except RuntimeError as re:
        print(f"Runtime Error: {re}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
