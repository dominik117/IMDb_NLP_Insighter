import requests
from bs4 import BeautifulSoup
import random
from time import sleep
import json
import os
import logging

# Constants
MAX_IDS = 10000000
SLEEP_MIN = 0.2
SLEEP_MAX = 1.0
BASE_URL = "https://www.imdb.com/title/tt{}"

USER_AGENTS = [
    # Google Chrome (Desktop)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    # Mozilla Firefox (Desktop)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0",
    # Apple Safari (Desktop)
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15",
    # Microsoft Edge (Desktop)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
    # Opera (Desktop)
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 OPR/76.0.4017.123",
]

logging.basicConfig(filename='app.log', filemode='w', level=logging.INFO)

session = requests.Session()

def fetch_single_movie_data(url_id):
    """Fetch data for a single movie given its URL ID."""
    url = BASE_URL.format(url_id)
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    try:
        response = session.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        if response.status_code == 200:
            return response.text, None
        else:
            return None, "No Data Inside"

    except requests.exceptions.HTTPError as he:
        if response.status_code != 404:
            logging.error(f"Error for {url_id}: {he}")

        if response.status_code == 429:  # Rate limit, increase sleep
            logging.error(f"Error for {url_id}: {he} | Sleep for 10 seconds")
            sleep(10)
        return None, str(he)

    except requests.exceptions.RequestException as error:
        logging.error(f"RequestException for {url}: {error}")
        return None, str(error)

def fetch_movie_data(start_idx=0, end_idx=MAX_IDS):
    """Fetch data for a range of movies."""
    raw_content = {}
    missing_movies = {}
    try:
        for i in range(start_idx, end_idx):
            url_id = str(i).zfill(len(str(MAX_IDS)) - 1)
            content, error = fetch_single_movie_data(url_id)

            if content:
                raw_content[url_id] = content
            if error:
                missing_movies[url_id] = error
            if (i + 1) % 100 == 0:
                logging.info(f"Processed {i + 1} movies")
            sleep(random.uniform(SLEEP_MIN, SLEEP_MAX))

    except KeyboardInterrupt:
        print("Fetching interrupted by user.")
        print(f"Last movie ID scraped: {i}")

    return raw_content, missing_movies


def save_to_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def main():
    raw_content, missing_movies = fetch_movie_data()
    save_to_json("raw_content.json", raw_content)
    save_to_json("missing_movies.json", missing_movies)

if __name__ == "__main__":
    main()
