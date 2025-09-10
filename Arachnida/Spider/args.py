import argparse

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Enable recursive download of images."
    )

    parser.add_argument(
        "-m",
        "--meta",
        action="store_true",
        help="checks for metadata and deletes them if they don't contain any."
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

    if not args.recursive and args.level != 5:
        parser.error("Option -l requires -r. Use -r -l [N] to set recursion depth.")

    return args
