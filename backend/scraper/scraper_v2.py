import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import time

visited = set()
site_data = []

def scrape_page(url, base_domain):
    print(f"Scraping: {url}")
    try:
        res = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        if res.status_code != 200:
            return

        soup = BeautifulSoup(res.text, 'html.parser')

        # Extract main text
        text_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        text = ' '.join([el.get_text(strip=True) for el in text_elements])

        # Extract table data
        tables = []
        for table in soup.find_all('table'):
            rows = []
            for tr in table.find_all('tr'):
                cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
                if cells:
                    rows.append(cells)
            if rows:
                tables.append(rows)

        # Extract images
        images = []
        for img in soup.find_all('img'):
            src = img.get('src')
            alt = img.get('alt', '')
            if src:
                images.append({'src': urljoin(url, src), 'alt': alt})

        # Extract internal links
        links = []
        for a in soup.find_all('a', href=True):
            full_link = urljoin(url, a['href'])
            if urlparse(full_link).netloc == base_domain:
                links.append(full_link)

        # Store content
        site_data.append({
            "url": url,
            "title": soup.title.string.strip() if soup.title else "",
            "text": text,
            "tables": tables,
            "images": images,
            "links": list(set(links))
        })

        return links

    except Exception as e:
        print(f"Error scraping {url}: {e}")

def crawl(url, depth=0, max_depth=2):
    base_domain = urlparse(url).netloc
    if url in visited or depth > max_depth:
        return
    visited.add(url)

    links = scrape_page(url, base_domain)
    if not links:
        return

    for link in links:
        if link not in visited:
            crawl(link, depth + 1, max_depth)

if __name__ == "__main__":
    base_url = "https://www.madewithnestle.ca"
    crawl(base_url, depth=0, max_depth=2)

    with open("scraper/nestle_full_scraped.json", "w") as f:
        json.dump(site_data, f, indent=2)

    print(f"\n✅ Done! Scraped {len(site_data)} pages.")
