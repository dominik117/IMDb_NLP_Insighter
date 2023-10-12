import logging
import requests
import sys
sys.path.append("scraper")
import data_fetcher
import data_storage
import utils

logging.basicConfig(
    filename='app.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    session = requests.Session()
    raw_content = data_storage.load_json_data("raw_content.json")
    missing_movies = data_storage.load_json_data("missing_movies.json")

    try:
        new_raw_content, new_missing_movies = data_fetcher.fetch_movie_data(
            start_idx=utils.find_latest_fetch(raw_content, missing_movies),
            session=session
        )

    except Exception as e:
        logging.error(f"Error during data fetching: {e}")
    else:
        raw_content.update(new_raw_content)
        missing_movies.update(new_missing_movies)

    finally:
        data_storage.save_to_json("raw_content.json", raw_content)
        data_storage.save_to_json("missing_movies.json", missing_movies)

if __name__ == "__main__":
    main()