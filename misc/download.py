#!/usr/bin/env python

from six.moves.urllib.request import urlopen
import subprocess
import os
import hashlib

def download_and_unzip(url, zip_file_path, target_folder):
    try:
        response = urlopen(url)
        with open(zip_file_path, 'wb') as out_file:
            while True:
                chunk = response.read(64 * 1024)  # 64 KB chunks
                if not chunk:
                    break
                out_file.write(chunk)
        print("Download completed successfully.")
    except Exception as e:
        print("Error downloading the file: {}".format(e))
        return

    # Calculate the actual size of the file
    actual_size = os.path.getsize(zip_file_path)
    print("Downloaded file size: {} bytes".format(actual_size))

    # Calculate MD5 hash of the downloaded file
    hash_md5 = hashlib.md5()
    with open(zip_file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    md5_hash = hash_md5.hexdigest()
    print("MD5 hash of the downloaded file: {}".format(md5_hash))

    # Unzip the file using subprocess and unzip command
    try:
        subprocess.check_call(["unzip", "-o", "-q", zip_file_path, "-d", target_folder])
        print("File successfully extracted to {}".format(target_folder))
    except subprocess.CalledProcessError as e:
        print("Failed to extract ZIP file: {}".format(e))


url = "https://storage.googleapis.com/sauce-devx-runners-bhtb/cypress-macos-amd64-8622143467.zip"
zip_file_path = 'cypress-macos-amd64-8622143467.zip'
target_folder = './' 

download_and_unzip(url, zip_file_path, target_folder)

