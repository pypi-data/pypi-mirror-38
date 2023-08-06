# filecompare
find duplicate files in a directory

### Usage

```
usage: filecompare [-h] [--raw] [--hash HASH] directory

Compare file content in directory

positional arguments:
  directory    dir to search, for all similar files

optional arguments:
  -h, --help   show this help message and exit
  --raw        easily parsable results
  --hash HASH  available hash algos: md5
  --delete     prompt user to delete replica files
```
