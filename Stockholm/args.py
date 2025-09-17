import argparse

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-r",
        "--reverse",
        type=str,
        help="Reverses the infection caused."
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s 1.0",
        help="Current Version running."
    )

    parser.add_argument(
        "-s",
        "--silent",
        action="store_true",
        help="silences the stdout of which files are affected."
    )

    args = parser.parse_args()


    return args
