import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import sys


def extract_links(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        links = []
        for anchor in soup.find_all('a', href=True):
            href = anchor.get('href')
            text = anchor.get_text(strip=True)
            
            absolute_url = urljoin(url, href)
            
            links.append({
                'href': href,
                'text': text if text else '(no text)',
                'absolute_url': absolute_url
            })
        
        return links
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None
    except Exception as e:
        print(f"Error parsing the webpage: {e}")
        return None


def get_links_only(links):
    if not links:
        return []
    return [link['absolute_url'] for link in links]
