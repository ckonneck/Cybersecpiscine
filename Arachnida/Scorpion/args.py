import argparse

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("file", help="The file you want to display the metadata off of.")

    args = parser.parse_args()

    return args
