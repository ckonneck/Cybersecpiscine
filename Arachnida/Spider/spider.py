from args import get_args
from utils import register_signal
from downloader import download_images, counters
import sys

if __name__ == "__main__":
    args = get_args()
    register_signal()

    print(f"Recursive: {args.recursive}")
    print(f"Max depth: {args.level}")
    print(f"Save path: {args.path}")
    print(f"URL: {args.url}")
    print(f"meta: {args.meta}")
    try:
        download_images(url=args.url, path=args.path, recursive=args.recursive, level=args.level, meta=args.meta)
    except KeyboardInterrupt:
        print("\nScraping interrupted by user. Exiting.")
        sys.exit(0)



    print("\nDownload summary:")
    print(f"Total images downloaded: {counters['downloaded']}")
    print(f"Total URLs skipped: {counters['skipped']}")
