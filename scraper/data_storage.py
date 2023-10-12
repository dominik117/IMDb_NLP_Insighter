import json
import os
import sys

def save_to_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

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