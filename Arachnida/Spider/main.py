#!/usr/bin/env python3

import argparse

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
from urllib.parse import urljoin
level = args.level
recursive = args.recursive
path = args.path
url = args.url


def download_images(url: str, path: str, recursive: bool, level: int):
    os.makedirs(path, exist_ok=True)
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    image_urls = [img.get("src") for img in soup.find_all("img") if img.get("src")]
    for img_url in image_urls:
        full_url = urljoin(url, img_url)
        filename = os.path.join(path, os.path.basename(full_url))
        try:
                    resp = requests.get(full_url, stream=True)
                    if resp.status_code == 200:
                        with open(filename, "wb") as f:
                            for chunk in resp.iter_content(1024):
                                f.write(chunk)
                        print(f"Saved {filename}")
        except Exception as e:
            print(f"Failed to download {full_url}: {e}")
    if level > 1:
        for link in soup.find_all("a", href=True):
            next_url = urljoin(url, link['href'])
            download_images(next_url, path, recursive, level-1)



    
download_images(
        url=args.url,
        path=args.path,
        recursive=args.recursive,
        level=args.level
    )