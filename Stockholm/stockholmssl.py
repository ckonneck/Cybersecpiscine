from args import get_args
from openssl import encryptionssl, decryptssl
import sys

if __name__ == "__main__":

    args = get_args()

    if not args.reverse:
        try:
            encryptionssl(args)
        except KeyboardInterrupt:
            print("\nProcess interrupted by user. Exiting.")
            sys.exit(0)
    else:
        try:
            decryptssl(args)
        except KeyboardInterrupt:
            print("\nProcess interrupted by user. Exiting.")
            sys.exit(0)
