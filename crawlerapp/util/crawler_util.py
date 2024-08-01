import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import xml.etree.ElementTree as ET
import re

def start_crawl(url):
    if is_valid_url(url):
        sitemap = crawl_website(url)
    
        #uncomment below to print the generate sitemap
        #print_sitemap(sitemap)

        #Generate an xml for the sitemap and save it
        xml_str = generate_xml_sitemap(sitemap)

        return "ok", xml_str
    else:
        return "error", "Invalid Url"
    
def is_valid_url(url):
    # Regular expression to validate a URL
    regex = re.compile(
        r'^(https?|ftp)://'  # http://, https://, or ftp://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'  # Domain name and extension
        r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'         # Domain extension
        r'localhost|'                                  # Localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'         # IPv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'                 # IPv6
        r'(?::\d+)?'                                   # Optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return re.match(regex, url) is not None

def crawl_website(start_url):
    base_domain = urlparse(start_url).netloc
    visited = set()
    queue = deque([start_url])
    sitemap = {}

    while queue:
        current_url = queue.popleft()
        
        if current_url in visited:
            continue
        
        # Uncomment for testing
        # if len(sitemap) > 20:
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
        print(f"-{url}")
        for anchor in soup.find_all("a", href=True):
            link = anchor.get("href")
            subpage = link.split('/')[-1]
            if subpage != "":
                print(f"\t- {subpage}")
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

def generate_xml_sitemap(sitemap):
    urlset = ET.Element("urlset", xmlns="http://www.sitemap-test.org/schemas/sitemap/0.9")
    for page, links in sitemap.items():
        url = ET.SubElement(urlset, "url")
        loc = ET.SubElement(url, "loc")
        loc.text = page

        for link in links:
            link_url = ET.SubElement(url, "url")
            loc_link = ET.SubElement(link_url, "loc")
            loc_link.text = link

    xml_sitemap = ET.ElementTree(urlset)
    return ET.tostring(xml_sitemap.getroot(), encoding='utf-8', method='xml')