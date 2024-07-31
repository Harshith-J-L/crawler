import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque

def start_crawl(url):
    sitemap = crawl_website(url)
    print_sitemap(sitemap)
    return "crawling completed"

def crawl_website(start_url):
    base_domain = urlparse(start_url).netloc
    visited = set()
    queue = deque([start_url])
    sitemap = {}

    while queue:
        current_url = queue.popleft()
        
        if current_url in visited:
            continue

        # if len(sitemap) > 10:
        #     break
        
        visited.add(current_url)
        links = get_all_links(current_url)
        sitemap[current_url] = []

        for link in links:
            if is_valid(link, base_domain):
                sitemap[current_url].append(link)
                if link not in visited:
                    queue.append(link)

    return sitemap

def get_all_links(url):
    # Extract all links from the given URL
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return []
        soup = BeautifulSoup(response.text, "html.parser")
        links = []
        for anchor in soup.find_all("a", href=True):
            link = anchor.get("href")
            full_url = urljoin(url, link)
            links.append(full_url)
        return links
    except requests.RequestException:
        return []

def is_valid(url, base_domain):
    # Check if the URL is valid and belongs to the base domain
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and parsed.netloc == base_domain

def print_sitemap(sitemap):
    for page, links in sitemap.items():
        print(f"-{page}")
        for link in links:
            subpage = link.split('/')[-1]
            if subpage != "":
                print(f"\t- {subpage}")