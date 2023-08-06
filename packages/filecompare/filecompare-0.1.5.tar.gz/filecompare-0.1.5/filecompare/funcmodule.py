import hashlib
import sys

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def hash_func(hash_algo, fname):
    if hash_algo.lower() == "md5":
        return md5(fname)
    else:
        print("ERROR: hash algo '{}' is not implemnted".format(hash_algo))
        sys.exit(1)