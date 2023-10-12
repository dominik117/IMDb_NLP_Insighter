import logging
import sys
import yaml

def load_config():
    try:
        with open('scraper/settings.yaml', 'r') as file:
            config = yaml.safe_load(file)["settings"]
        return config
    except KeyError as ke:
        logging.error(f"Missing key in configuration: {ke}")
        sys.exit(1)