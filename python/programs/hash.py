#!/usr/bin/env python3

import hashlib, sys

def sha256_checksum(file_path):
    """
    Generate SHA-256 checksum for a large file using hashlib.file_digest.

    :param file_path: Path to the file.
    :return: SHA-256 checksum as a hexadecimal string.
    """
    # Open the file in binary mode and compute its SHA-256 checksum
    with open(file_path, 'rb') as f:
        file_hash = hashlib.file_digest(f, 'sha256')

    return file_hash.hexdigest()

def sha256_checksum2(file_path, chunk_size=8192):
    sha256 = hashlib.sha256()
    
    with open(file_path, 'rb') as f:
        while chunk := f.read(chunk_size):
            sha256.update(chunk)
    
    return sha256.hexdigest()


# Example usage
file_path = sys.argv[1]
checksum = sha256_checksum(file_path)
print(f"SHA-256 checksum: {checksum}")
checksum = sha256_checksum2(file_path)
print(f"SHA-256 checksum 2: {checksum}")

