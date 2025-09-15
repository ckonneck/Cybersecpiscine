import argparse

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-r",
        "--reverse",
        action="store_true",
        help="Reverses the infection caused."
    )

    parser.add_argument(
        "-v",
        "--version",
        type=float,
        default=1,
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
