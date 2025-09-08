#!/usr/bin/env python3

import argparse
import signal
import sys

# Global flag to stop recursion
stop_scraping = False

def signal_handler(sig, frame):
    global stop_scraping
    print("\n Received Ctrl+C! Stopping the downloads...")
    stop_scraping = True

# Register the handler
signal.signal(signal.SIGINT, signal_handler)

parser = argparse.ArgumentParser()
# Flags
parser.add_argument(
    "-r",
    "--recursive",
    action="store_true",
    help="Enable recursive download of images."
)

parser.add_argument(
    "-l",
    "--level",
    type=int,
    default=5,
    help="Maximum recursion depth (default: 5). Only used with -r."
)

parser.add_argument(
    "-p",
    "--path",
    default="./data/",
    help="Path to save downloaded files (default: ./data/)."
)

parser.add_argument("url", help="URL of the website to scrape.")

args = parser.parse_args()

if not args.recursive and "level" in args and args.level != 5:
    parser.error("Option -l requires -r. Use -r -l [N] to set recursion depth.")

print("Recursive:", args.recursive)
print("Max depth:", args.level)
print("Save path:", args.path)
print("URL:", args.url)

# Your logic can then be:
if args.recursive:
    print(f"Will download images recursively up to depth {args.level}")
else:
    print("Will download only top-level images")

from bs4 import BeautifulSoup
import requests
import os
from urllib.parse import urljoin, urlparse
level = args.level
recursive = args.recursive
path = args.path
url = args.url


ALLOWED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".bmp")
downloaded_urls = set()
downloaded_count = 0
skipped_count = 0

def download_images(url: str, path: str, recursive: bool, level: int, visited=None):
    global stop_scraping, downloaded_count, skipped_count
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
    except Exception as e:
        return

    soup = BeautifulSoup(html, "html.parser")

    # find all image sources
    image_urls = [img.get("src") for img in soup.find_all("img") if img.get("src")]


    for img_url in image_urls:
        full_url = urljoin(url, img_url)
        filename = os.path.join(path, os.path.basename(urlparse(full_url).path) or "image.jpg")
        if full_url in downloaded_urls:
            skipped_count += 1
            continue
        # Only download allowed types
        if not full_url.lower().endswith(ALLOWED_EXTENSIONS):
            print(f"Skipping {full_url}")
            skipped_count += 1
            continue
        
        downloaded_urls.add(full_url)
        downloaded_count += 1


        try:
            img_resp = requests.get(full_url, stream=True, timeout=10)
            if img_resp.status_code == 200 and img_resp.headers.get("Content-Type", "").startswith("image/"):
                with open(filename, "wb") as f:
                    for chunk in img_resp.iter_content(8192):  # 8KB chunks
                        f.write(chunk)
                print(f"Saved {filename}")
        except Exception as e:
            print(f"Failed to download {full_url}: {e}")

    # recurse if enabled and depth allows
    if recursive and level > 1:
        for link in soup.find_all("a", href=True):
            next_url = urljoin(url, link["href"])
            # only follow same-domain links
            if urlparse(next_url).netloc == urlparse(url).netloc:
                download_images(next_url, path, recursive, level - 1, visited)


if __name__ == "__main__":
    try:
        download_images(url=args.url, path=args.path, recursive=args.recursive, level=args.level)
    except KeyboardInterrupt:
        print("\nScraping interrupted by user. Exiting.")
        sys.exit(0)

    print("\nDownload summary:")
    print(f"Total images downloaded: {downloaded_count}")
    print(f"Total URLs skipped: {skipped_count}")