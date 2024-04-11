#!/usr/bin/env python

from six.moves.urllib.request import urlopen
import subprocess
import os
import hashlib

def download_and_unzip(url, zip_file_path, target_folder):
    # Download the file in chunks
    try:
        with urlopen(url) as response:
            with open(zip_file_path, 'wb') as out_file:
                while True:
                    chunk = response.read(64 * 1024)
                    if not chunk:
                        break
                    out_file.write(chunk)
        print("Download completed successfully.")
    except Exception as e:
        print("Error downloading the file:", e)
        return

    actual_size = os.path.getsize(zip_file_path)
    print('file size: ', actual_size)

    hash_md5 = hashlib.md5()
    with open(zip_file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    md5_hash = hash_md5.hexdigest()
    print('md5sum: ', md5_hash)

    try:
        subprocess.check_call(["unzip", "-o", "-q", zip_file_path, "-d", target_folder])
        print("File successfully extracted")
    except subprocess.CalledProcessError as e:
        print("Failed to extract ZIP file: ", e)

# Example usage
url = "https://storage.googleapis.com/sauce-devx-runners-bhtb/cypress-macos-amd64-8622143467.zip"
zip_file_path = 'cypress-macos-amd64-8622143467.zip'
target_folder = './' 

download_and_unzip(url, zip_file_path, target_folder)

