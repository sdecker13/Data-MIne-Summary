import nltk
nltk.download('popular')
import requests
from bs4 import BeautifulSoup

def fetch_article(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the main content of the article
        # Note: This selector might need to be adjusted based on the specific website structure
        article_body = soup.find('div', class_='article-body')
        
        if article_body:
            # Extract all paragraph texts
            paragraphs = article_body.find_all('p')
            article_text = ' '.join([p.get_text() for p in paragraphs])
            return article_text
        else:
            return "Could not find article content."
    else:
        return f"Failed to retrieve the article. Status code: {response.status_code}"
