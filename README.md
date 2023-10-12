# IMDB Movie Scraper

This script is designed to scrape all movie content from IMDB based on movie URL IDs.

## Key Features:

- **Keyboard Interrupt Handling**: The script supports a keyboard interrupt to pause the scraping. If interrupted, it can continue where it left off during the next run by loading the already scraped pages.

## Requirements

- Python
- `virtualenv` (recommended for creating a virtual environment)

## Setting Up a Virtual Environment (Recommended)

1. Install `virtualenv` if not installed:

   ```bash
   pip install virtualenv
   ```

2. Navigate to the project's root directory and create a virtual environment:

   ```bash
   virtualenv venv
   ```

3. Activate the virtual environment:

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

   - On Windows:

     ```bash
     .\venv\Scripts\activate
     ```

4. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

5. Deactivate the virtual environment when done:

   ```bash
   deactivate
   ```

## Usage

1. Ensure you're in the virtual environment (as per the steps above).
2. Execute the script:

   ```bash
   python -m scraper.main
   ```

## Settings and Constants:

- `MAX_IDS` - Maximum number of IDs to fetch, set to 9,999,999 which is the maximun length of the current movie IDs.
- `SLEEP_MIN` and `SLEEP_MAX` - Minimum and maximum time (in seconds) the scraper will wait between requests.
- `BASE_URL` - IMDB base URL format string.
- `USER_AGENTS` - List of user-agent strings for rotating headers for the request and ensuring not being blocked.

## Output

The script will generate (or update, if they already exist) two JSON files:

- `raw_content.json`: Contains the raw HTML content of fetched movies. The movie ID acts as the key.
- `missing_movies.json`: Contains movies that couldn't be fetched, with an error message for each. The movie ID acts as the key.

## Logs

The script logs its operations in `app.log`. Check this file for any issues or errors encountered during the scraping process.

## Important Notes

- Web scraping might be against the terms of service of the website. Always ensure you have the right to scrape a website and that you respect the website's `robots.txt` file.
- According to the [IMDB robots.txt](https://www.imdb.com/robots.txt) file, scraping the title directory, where the general movie information is located, is permitted.
- This script might be subjected to IP bans if overused. Always use web scraping scripts responsibly and ethically.

## Disclaimer

This tool is meant for educational purposes only. The user is responsible for any potential misuse or breaches of terms of service.

## Contribution

Feel free to contribute or suggest any improvements to this tool. Make sure to test your changes thoroughly before submitting a pull request.