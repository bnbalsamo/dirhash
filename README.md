# dirhash [![v0.1.0](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/bnbalsamo/dirhash/releases)

[![Build Status](https://travis-ci.org/bnbalsamo/dirhash.svg?branch=master)](https://travis-ci.org/bnbalsamo/dirhash) [![Coverage Status](https://coveralls.io/repos/github/bnbalsamo/dirhash/badge.svg?branch=master)](https://coveralls.io/github/bnbalsamo/dirhash?branch=master) [![Documentation Status](https://readthedocs.org/projects/dirhash/badge/?version=latest)](http://dirhash.readthedocs.io/en/latest/?badge=latest) [![Updates](https://pyup.io/repos/github/bnbalsamo/dirhash/shield.svg)](https://pyup.io/repos/github/bnbalsamo/dirhash/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Produce a checksum, similar to a hash, for directories.

See the full documentation at https://dirhash.readthedocs.io

# Installation
- ```$ git clone https://github.com/bnbalsamo/dirhash.git```
- ```$ cd dirhash```
    - If you would like to install the pinned dependencies, run ```pip install -r requirements.txt```
- ```$ python setup.py install```

# Usage
```
$ dirhash --help
Usage: dirhash [OPTIONS] PATH

  Produce the hash of a file or directory.

  Directory 'hashes', much like file hashes, when compared, can confirm that
  each contains an identical series of bytes. In the case of the directory
  'hash' these bytes must be an identical set of files, but all attributes
  of the files except their contents is ignored.

Options:
  -a, --algorithm                 The name of the algorithm to use to generate
                                  the checksum. Default: md5

  -c, --chunksize INTEGER         How many bytes of files to read into RAM at
                                  once while generating checksums. Default:
                                  1000000

  --resolve-symlinks / --dont-resolve-symlinks
                                  Whether or not to resolve symlinks while
                                  generating checksums and traversing the file
                                  system. Default: True

  --help                          Show this message and exit.
```

# Implementation

In order to produce a checksum for directories `dirhash` recursively walks
the directory structure.

In the base case, where a directory is empty or
contains no subdirectories, its contents are hashed, those hashes are
sorted, and the hash of a string that results from concatenating those
results together is returned as the hash of the directory.

In directories which include subdirectories the "dirhash" of the
subdirectory is computed and used in place of a file hash.

# Development

## Installing Development Dependencies

```
$ pip install -r requirements/requirements_dev.txt
```

## Running Tests
```
$ tox
```
Note: Tox will run tests against the version of the software installed via ```python setup.py install```.

To test against pinned dependencies add ```-r requirements.txt``` to the deps array of the tox.ini testenv
section.

## Running autoformatters

- ```tox -e run_black,run_isort```

## Pinning Dependencies
- ```pip install -r requirements/requirements_dev.txt```
- ```tox -e pindeps```

# Author
Brian Balsamo <Brian@BrianBalsamo.com>
