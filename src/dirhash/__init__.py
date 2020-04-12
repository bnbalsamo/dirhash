"""dirhash: Produce a checksum, similar to a hash, for directories."""

__author__ = "Brian Balsamo"
__email__ = "brian@brianbalsamo.com"
__version__ = "0.1.0"


from hashlib import algorithms_available, new
from pathlib import Path

import click


def hash_file(path, chunksize=1000000, algo="md5"):
    """
    Produce the hexdigest of the hash of a file.

    :param pathlib.Path path: The filepath to the file to be hashed
    :param int chunksize: The maximum amount of the file to read into RAM at once,
        in bytes.
    :param str algo: The hashing algorithm to use, passed to :func:`hashlib.new`
    :returns: A :class:`_hashlib.HASH` object containing the hash of the file
    :rtype: str
    """
    hasher = new(algo)
    with open(path, "rb") as file_handle:
        chunk = file_handle.read(chunksize)
        while chunk:
            hasher.update(chunk)
            chunk = file_handle.read(chunksize)
    return hasher.hexdigest()


def hash_dir(path, chunksize=1000000, algo="md5", resolve_symlinks=True):
    """
    Produce the hexdigest of the 'hash' of a directory recursively.

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
    subhashes = []

    for entry in path.iterdir():
        if resolve_symlinks:
            entry = entry.resolve()
        if entry.is_file():
            subhashes.append(hash_file(entry, chunksize=chunksize, algo=algo))
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
    # Pseudo-bytestream
    dir_data = b" ".join([x.encode("utf-8") for x in sorted_subhashes])
    hasher = new(algo)
    hasher.update(dir_data)
    return hasher.hexdigest()


def hash_entry(path, chunksize=1000000, algo="md5", resolve_symlinks=True):
    """
    Produce the hash of a file or directory.

    See hash_{file,dir} for more information.

    :param pathlib.Path path: The path to the directory to hash
    :param int chunksize: The maximum amount of any file to read into RAM at once,
        in bytes
    :param str algo: The hashing algorithm to use, passed to :func:`hashlib.new`
    :param bool resolve_symlinks: Whether or not to resolve symlinks.
    """
    if resolve_symlinks:
        path = path.resolve()

    if path.is_file():
        return hash_file(path, chunksize=chunksize, algo=algo)
    if path.is_dir():
        return hash_dir(
            path, chunksize=chunksize, algo=algo, resolve_symlinks=resolve_symlinks
        )
    raise AssertionError("%s is not a file or directory!" % path)


@click.command()
@click.argument(
    "path", type=click.Path(exists=True), required=True,
)
@click.option(
    "-a",
    "--algorithm",
    type=click.Choice(algorithms_available),
    default="md5",
    help="The name of the algorithm to use to generate the checksum. Default: md5",
)
@click.option(
    "-c",
    "--chunksize",
    type=int,
    default=1000000,
    help="How many bytes of files to read into RAM at once while generating "
    "checksums. Default: 1000000",
)
@click.option(
    "--resolve-symlinks/--dont-resolve-symlinks",
    default=True,
    help="Whether or not to resolve symlinks while generating checksums "
    "and traversing the file system. Default: True",
)
def cli(path, algorithm, chunksize, resolve_symlinks):
    """
    Produce the hash of a file or directory.

    Directory 'hashes', much like file hashes, when compared, can confirm
    that each contains an identical series of bytes. In the case of
    the directory 'hash' these bytes must be an identical set of files,
    but all attributes of the files except their contents is ignored.
    """
    path = Path(path)
    click.echo(
        hash_entry(
            path,
            chunksize=chunksize,
            algo=algorithm,
            resolve_symlinks=resolve_symlinks,
        )
    )
