from bs4 import BeautifulSoup

def parse_movie_data(content):
    """Parses movie data from the fetched content."""
    soup = BeautifulSoup(content, "html.parser")
    main_content = soup.find('main', attrs={"role": "main"})
    section_content = main_content.find('div').find('section')
    return str(section_content) if section_content else None
