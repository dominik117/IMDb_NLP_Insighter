from bs4 import BeautifulSoup

def parse_movie_data(content):
    """Parses movie data from the fetched content."""
    soup = BeautifulSoup(content, "html.parser")
    main_content = soup.find('main', attrs={"role": "main"})
    return str(main_content) if main_content else None
