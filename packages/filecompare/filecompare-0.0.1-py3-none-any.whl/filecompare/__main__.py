import os
from .funcmodule import hash_func
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Compare file content in directory')
    parser.add_argument('--raw', dest='raw', action='store_true', help='easily parsable results')
    parser.add_argument('--hash', action='store', type=str, default="md5", help='available hash algos: md5')
    parser.add_argument('directory', type=str, help='dir to search, for all similar files')
    return parser.parse_args()

def main():
    args = parse_args()
    hashes = {}
    dirname = args.directory.rstrip("/")

    # Get all files in all sub directories
    for dir, dirname, filename in os.walk(dirname):
        for f in filename:
            file_path = dir + "/" + f
            hash = hash_func(args.hash, file_path)
            if hash in hashes:
                hashes[hash].append(file_path)
            else:
                hashes[hash] = [file_path]

    # Display duplicate hashes
    for k, v in hashes.items():
        if len(v) > 1:
            if args.raw:
                print("{}".format(",".join(v)))
            else:
                print("{}: ".format(len(v)) + "\n\t-".join(v))



if __name__ == "__main__":
    main()

