import os
from .funcmodule import hash_func
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Compare file content in directory')
    parser.add_argument('--raw', dest='raw', action='store_true', help='easily parsable results')
    parser.add_argument('--hash', action='store', type=str, default="md5", help='available hash algos: md5')
    parser.add_argument('--delete', dest='delete', action='store_true', help='prompt user to delete replica files')
    parser.add_argument('directory', type=str, help='dir to search, for all similar files')
    return parser.parse_args()

def main():
    args = parse_args()
    hashes = {}
    duplicate_hashes = {}
    dirname = args.directory.rstrip("/")

    # Get all files in all sub directories
    for dir, dirname, filename in os.walk(dirname):
        for f in filename:
            file_path = dir + "/" + f
            hash = hash_func(args.hash, file_path)
            if hash in hashes:
                # sort the array smallest first
                if len(file_path) < len(hashes[hash][0]):
                    hashes[hash].insert(0, file_path)
                else:
                    hashes[hash].append(file_path)
                duplicate_hashes[hash] = hashes[hash]
            else:
                hashes[hash] = [file_path]

    del hashes

    # Display duplicate hashes
    for hash, paths in duplicate_hashes.items():
        if args.raw:
            print("{}".format(",".join(paths)))
        else:
            print("{}: {}".format(len(paths), "\n\t-".join(paths)))

    if args.delete:
        for hash, paths in duplicate_hashes.items():
            i = 0
            print("##################################")
            for path in paths:
                print("[{}]: {}".format(i, path))
                i += 1
            excluded_files = input("excluded files[0]: ")
            if excluded_files == "":
                excluded_files = "0"
            excluded_files = excluded_files.split(" ")
            print("exclused files: {}".format(excluded_files))
            i = 0
            for path in paths:
                if str(i) not in excluded_files:
                    os.remove(path)
                    print("removed {}".format(path))
                i += 1





if __name__ == "__main__":
    main()

