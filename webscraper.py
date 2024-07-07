import requests
from bs4 import BeautifulSoup

def fetch_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        page_text = soup.get_text()
        return page_text

    except requests.exceptions.RequestException as e:
        return f"Error fetching page content: {e}"
