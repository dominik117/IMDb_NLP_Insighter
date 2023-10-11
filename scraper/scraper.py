import os
import sys
import json
import random
import logging
import requests
from time import sleep
from bs4 import BeautifulSoup
import yaml

logging.basicConfig(
    filename='app.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_config():
    try:
        with open('scraper/settings.yaml', 'r') as file:
            config = yaml.safe_load(file)["settings"]
        return config
    except KeyError as ke:
        logging.error(f"Missing key in configuration: {ke}")
        sys.exit(1)

CONFIG = load_config()
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

def parse_movie_data(content):
    """Parses movie data from the fetched content."""
    soup = BeautifulSoup(content, "html.parser")
    main_content = soup.find('main', attrs={"role": "main"})
    return str(main_content) if main_content else None

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
                movie_data = parse_movie_data(content)
                if movie_data:
                    raw_content[url_id] = movie_data
                else:
                    missing_movies[url_id] = "No Content Found"
            if error:
                missing_movies[url_id] = error
            if (i + 1) % 200 == 0:
                logging.info(f"Processed {i + 1} movies")
                print(f"Processed {i + 1} movies")
            sleep(random.uniform(SLEEP_MIN, SLEEP_MAX))

    except KeyboardInterrupt:
        print("\nFetching interrupted by user.")
        print(f"Last movie ID scraped: {i-1}")
    return raw_content, missing_movies

def load_json_data(filename):
    """Load data from JSON if it exists."""
    try:
        if os.path.exists(filename):
            print(f"Loading existing data from {filename}...")
            with open(filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        return {}

    except KeyboardInterrupt:
        print("\nFetching interrupted by user before loading the data.")
        sys.exit("Terminating the script to avoid data loss.")

def save_to_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def find_latest_fetch(*args):
    highest_id = 0
    for data in args:
        latest_id = max(map(int, data.keys())) if data else 0
        if latest_id > highest_id:
            highest_id = latest_id 
    return highest_id

def main():
    session = requests.Session()
    raw_content = load_json_data("raw_content.json")
    missing_movies = load_json_data("missing_movies.json")

    try:
        new_raw_content, new_missing_movies = fetch_movie_data(
            start_idx=find_latest_fetch(raw_content, missing_movies),
            session=session
        )

    except Exception as e:
        logging.error(f"Error during data fetching: {e}")
    else:
        raw_content.update(new_raw_content)
        missing_movies.update(new_missing_movies)

    finally:
        save_to_json("raw_content.json", raw_content)
        save_to_json("missing_movies.json", missing_movies)

if __name__ == "__main__":
    main()