import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
from storage import save_page
import hashlib

def hash_url(url):
    return hashlib.sha256(url.encode()).hexdigest()

def crawl(seed_url, page_limit=1000, token_limit=500):
    queue = deque([seed_url])
    visited = set()
    count = 0

    while queue and count < page_limit:
        url = queue.popleft()
        if url in visited:
            continue

        try:
            response = requests.get(url, timeout=5)
            if 'text/html' not in response.headers.get('Content-Type', ''):
                continue
            
            soup = BeautifulSoup(response.content, 'lxml')
            title = soup.title.string if soup.title else url
            body_text = soup.get_text(separator=' ', strip=True) if soup.body else ''
            tokens = " ".join(body_text.split()[:token_limit])

            save_page(url, title, tokens)
            visited.add(url)
            count += 1
            print(f"[{count}] Crawled: {url}")

            for link in soup.find_all('a', href=True):
                absolute_url = urljoin(url, link['href'])
                if urlparse(absolute_url).scheme.startswith('http') and absolute_url not in visited:
                    queue.append(absolute_url)

        except requests.RequestException as e:
            print(f"Error crawling {url}: {e}")
        