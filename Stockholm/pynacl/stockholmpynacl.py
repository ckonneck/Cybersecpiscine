from args import get_args
from pynacl import encryptpynacl, decryptpynacl
import sys

if __name__ == "__main__":

    args = get_args()

    if not args.reverse:
        try:
            encryptpynacl(args)
        except KeyboardInterrupt:
            print("\nProcess interrupted by user. Exiting.")
            sys.exit(0)
    else:
        try:
            decryptpynacl(args)
        except KeyboardInterrupt:
            print("\nProcess interrupted by user. Exiting.")
            sys.exit(0)
