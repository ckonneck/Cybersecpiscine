import os
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from utils import stop_scraping
from metacheck import meta_check

ALLOWED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".bmp")

downloaded_urls = set()

counters = {"downloaded": 0, "skipped": 0}

def download_images(url: str, path: str, recursive: bool, level: int, meta: bool, visited=None):
    global downloaded_urls, stop_scraping
    if stop_scraping:
        return

    if visited is None:
        visited = set()
    if url in visited:
        return
    visited.add(url)

    os.makedirs(path, exist_ok=True)

    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        html = resp.text
    except:
        return

    soup = BeautifulSoup(html, "html.parser")
    image_urls = [img.get("src") for img in soup.find_all("img") if img.get("src")]

    for img_url in image_urls:
        full_url = urljoin(url, img_url)
        filename = os.path.join(path, os.path.basename(urlparse(full_url).path) or "image.jpg")

        if full_url in downloaded_urls:
            counters["skipped"] += 1
            continue

        if not full_url.lower().endswith(ALLOWED_EXTENSIONS):
            print(f"Skipping {full_url}")
            counters["skipped"] += 1
            continue

        downloaded_urls.add(full_url)
        counters["downloaded"] += 1

        try:
            img_resp = requests.get(full_url, stream=True, timeout=10)
            if img_resp.status_code == 200 and img_resp.headers.get("Content-Type", "").startswith("image/"):
                with open(filename, "wb") as f:
                    for chunk in img_resp.iter_content(8192):
                        f.write(chunk)
                print(f"Saved {filename}")
            if meta:
                meta_check(filename)
        except Exception as e:
            print(f"Failed to download {full_url}: {e}")

    if recursive and level > 1:
        for link in soup.find_all("a", href=True):
            next_url = urljoin(url, link["href"])
            if urlparse(next_url).netloc == urlparse(url).netloc:
                download_images(next_url, path, recursive, level - 1, visited)
