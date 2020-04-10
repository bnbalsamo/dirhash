"""dirhash: Produce a checksum, similar to a hash, for directories."""

__author__ = "Brian Balsamo"
__email__ = "brian@brianbalsamo.com"
__version__ = "0.0.1"


import argparse
import sys
from hashlib import new
from pathlib import Path


def checksum(path, chunksize=1000000, algo="md5"):
    """
    Produce a hashlib.hash object which contains the checksum of a file.

    :param pathlib.Path path: The filepath to the file to be hashed
    :param int chunksize: The maximum amount of the file to read into RAM at once,
        in bytes.
    :param str algo: The hashing algorithm to use, passed to :func:`hashlib.new`
    :returns: A :class:`_hashlib.HASH` object containing the hash of the file
    :rtype: :class:`_hashlib.HASH`
    """
    hasher = new(algo)
    with open(path, "rb") as file_handle:
        chunk = file_handle.read(chunksize)
        while chunk:
            hasher.update(chunk)
            chunk = file_handle.read(chunksize)
    return hasher


def get_parser():
    """
    Create the parser for the CLI.

    :returns: The parser
    :rtype: :class:`argparse.ArgumentParser`
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("directory", type=str, help="The path to the directory to hash")
    parser.add_argument(
        "-c",
        "--chunksize",
        type=int,
        default=1000000,
        help="How many bytes (maximum) of a file to read into RAM at once",
    )
    parser.add_argument(
        "-a",
        "--algo",
        type=str,
        default="md5",
        help="The algorithm to employ internally for generating the checksum",
    )
    parser.add_argument(
        "--dont-resolve-symlinks",
        action="store_true",
        default=False,
        help="Whether or not to resolve symlinks in the directory.",
    )
    return parser


def hash_dir(path, chunksize=1000000, algo="md5", resolve_symlinks=True):
    """
    Produce the 'hash' of a directory recursively.

    Directory 'hashes', much like file hashes, when compared, can confirm
    that each contains an identical series of bytes. In the case of
    the directory 'hash' these bytes must be an identical set of files,
    but all attributes of the files except their contents is ignored.

    :param pathlib.Path path: The path to the directory to hash
    :param int chunksize: The maximum amount of any file to read into RAM at once,
        in bytes
    :param str algo: The hashing algorithm to use, passed to :func:`hashlib.new`
    :param bool resolve_symlinks: Whether or not to resolve symlinks.
    """
    if resolve_symlinks:
        path = path.resolve()

    if not path.is_dir():
        raise AssertionError("%s is not a directory!" % path)

    subhashes = []

    for entry in path.iterdir():
        if resolve_symlinks:
            entry = entry.resolve()
        if entry.is_file():
            subhashes.append(
                checksum(entry, chunksize=chunksize, algo=algo).hexdigest()
            )
        elif entry.is_dir():
            subhashes.append(
                hash_dir(
                    entry,
                    chunksize=chunksize,
                    algo=algo,
                    resolve_symlinks=resolve_symlinks,
                )
            )
        else:
            raise AssertionError("%s is not a file or directory!" % entry)

    sorted_subhashes = sorted(subhashes)
    dir_data = b" ".join([x.encode("utf-8") for x in sorted_subhashes])
    hasher = new(algo)
    hasher.update(dir_data)
    return hasher.hexdigest()


def main(args):
    """
    Ingest the arguments, generate the directory hash.

    :param argparse.Namespace args: The parsed arguments
    :returns: A :class:`_hashlib.HASH` object containing the hash of the directory
    :rtype: :class:`_hashlib.HASH`
    """
    dir_hash = hash_dir(
        Path(args.directory),
        chunksize=args.chunksize,
        algo=args.algo,
        resolve_symlinks=not args.dont_resolve_symlinks,
    )
    return dir_hash


def cli():
    """
    Return the CLI interface entrypoint.

    Get the parser, parse the args, call :func:`main`, write out the hexdigest.
    """
    parser = get_parser()
    args = parser.parse_args()

    dir_hash = main(args)

    sys.stdout.write("{}\n".format(dir_hash))
    sys.exit(0)


if __name__ == "__main__":
    cli()
