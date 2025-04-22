import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
import logging

# Configure logging
event_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=event_format)

class WebScraper:
    def __init__(self, urls, output, timeout=10):
        self.urls = urls
        self.output = output
        self.timeout = timeout
        self.session = requests.Session()
        # Optional: Add retries, headers, etc.
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; WebScraper/1.0)'
        })
        self.results = []

    def scrape_page(self, url):
        try:
            resp = self.session.get(url, timeout=self.timeout)
            resp.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"Failed to fetch {url}: {e}")
            return None

        soup = BeautifulSoup(resp.text, 'html.parser')
        # Safely extract title text
        title_tag = soup.title
        title_text = title_tag.get_text(strip=True) if title_tag else None

        # Safely extract meta description
        meta_desc = None
        meta_tag = soup.find('meta', attrs={'name': 'description'})
        if meta_tag and meta_tag.get('content'):
            meta_desc = meta_tag['content'].strip()

        data = {
            'url': url,
            'title': title_text,
            'meta_description': meta_desc,
            'headings': [],
            'paragraphs': [],
            'links': [],
            'images': []
        }

        # Headings h1-h6
        for level in range(1, 7):
            for tag in soup.find_all(f'h{level}'):
                text = tag.get_text(strip=True)
                if text:
                    data['headings'].append(text)
        data['headings'].sort()

        # Paragraphs
        for p in soup.find_all('p'):
            text = p.get_text(strip=True)
            if text:
                data['paragraphs'].append(text)

        # Links
        for a in soup.find_all('a', href=True):
            href = urljoin(url, a['href'])
            text = a.get_text(strip=True)
            data['links'].append({'text': text, 'url': href})
        data['links'].sort(key=lambda x: x['url'])

        # Images
        for img in soup.find_all('img', src=True):
            src = urljoin(url, img['src'])
            alt = img.get('alt', '').strip()
            data['images'].append({'url': src, 'alt': alt})

        logging.info(f"Scraped {url}")
        return data

    def run(self):
        for url in self.urls:
            url = url.strip()
            if not url or url.startswith('#'):
                continue
            result = self.scrape_page(url)
            if result:
                self.results.append(result)

        # Save results
        try:
            with open(self.output, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, ensure_ascii=False, indent=2)
            logging.info(f"Saved results to {self.output}")
        except IOError as e:
            logging.error(f"Failed to write output file: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generic web scraper')
    parser.add_argument('-u', '--urls', default='urls.txt', help='Path to file containing URLs (one per line)')
    parser.add_argument('-o', '--output', default='scraped_data.json', help='Output JSON file')
    parser.add_argument('-t', '--timeout', type=int, default=10, help='Request timeout in seconds')
    args = parser.parse_args()

    # Read URL list
    try:
        with open(args.urls, 'r', encoding='utf-8') as f:
            url_list = f.readlines()
    except FileNotFoundError:
        logging.error(f"URL file not found: {args.urls}")
        exit(1)

    scraper = WebScraper(urls=url_list, output=args.output, timeout=args.timeout)
    scraper.run()
