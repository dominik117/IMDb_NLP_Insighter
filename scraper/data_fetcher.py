import logging
import random
import requests
import sys
from time import sleep
sys.path.append("scraper")
import config
import data_parser

CONFIG = config.load_config()
MAX_IDS = CONFIG["MAX_IDS"]
USER_AGENTS = CONFIG["USER_AGENTS"]
SLEEP_MIN = CONFIG["SLEEP_MIN"]
SLEEP_MAX = CONFIG["SLEEP_MAX"]
BASE_URL = CONFIG["BASE_URL"]

def get_random_user_agent():
    """Return a random user agent from a predefined list."""
    return random.choice(USER_AGENTS)

def fetch_url_content(url, session):
    """Fetches content for a given URL."""
    headers = {'User-Agent': get_random_user_agent()}
    try:
        response = session.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.text, None

    except requests.exceptions.HTTPError as he:
        if response.status_code != 404:
            logging.error(f"Error for {url_id}: {he}")
        if response.status_code == 429:
            logging.error(f"Rate limited for {url_id}: {he} \nSleeping for 10 seconds.")
            sleep(10)
        return None, str(he)

    except requests.exceptions.RequestException as error:
        logging.error(f"RequestException for {url_id}: {error}")
        return None, str(error)

def fetch_movie_data(start_idx=0, end_idx=MAX_IDS, session=None):
    """Fetch data for a range of movies."""
    raw_content = {}
    missing_movies = {}

    try:
        print("Scraping initialized...")
        for i in range(start_idx, end_idx):
            url_id = str(i).zfill(len(str(MAX_IDS)) - 1)
            url = BASE_URL.format(url_id)
            content, error = fetch_url_content(url, session)

            if content:
                movie_data = data_parser.parse_movie_data(content)
                if movie_data:
                    raw_content[url_id] = movie_data
                else:
                    missing_movies[url_id] = "No Content Found"
            if error:
                missing_movies[url_id] = error
            if (i + 1) % 500 == 0:
                logging.info(f"Processed {i + 1} movies")
                print(f"Processed {i + 1} movies")
            sleep(random.uniform(SLEEP_MIN, SLEEP_MAX))

    except KeyboardInterrupt:
        print("\nFetching interrupted by user.")
        print(f"Last movie ID scraped: {i-1}")
    return raw_content, missing_movies