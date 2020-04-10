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
usage: dirhash [-h] [-c CHUNKSIZE] [-a ALGO] [--dont-resolve-symlinks]
               directory

positional arguments:
  directory             The path to the directory to hash

optional arguments:
  -h, --help            show this help message and exit
  -c CHUNKSIZE, --chunksize CHUNKSIZE
                        How many bytes (maximum) of a file to read into RAM at
                        once
  -a ALGO, --algo ALGO  The algorithm to employ internally for generating the
                        checksum
  --dont-resolve-symlinks
                        Whether or not to resolve symlinks in the directory.
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

- ```tox -e run_black,run_isort

## Pinning Dependencies
- ```pip install -r requirements/requirements_dev.txt```
- ```tox -e pindeps```

# Author
Brian Balsamo <Brian@BrianBalsamo.com>
