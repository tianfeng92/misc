#!/usr/bin/env python

from six.moves.urllib.request import urlopen
import subprocess
import os
import hashlib
import threading

READ_BUFFER_SIZE_BYTES = 64*1024
timeout = 35

class ResponseReaderInfo(object):
    def __init__(self):
        self.did_read_all_data = False
        self.last_exception = None


class FileIntegrityError(Exception):
    pass

def download_and_unzip(url, zip_file_path, target_folder):
    try:
        response = urlopen(url)
        print("resp: ", response.getcode())
        with open(zip_file_path, "wb") as f:
                while True:
                    rr_info = ResponseReaderInfo()

                    def read_next_chunk():
                        try:
                            chunk = response.read(READ_BUFFER_SIZE_BYTES)
                            if chunk:
                                f.write(chunk)
                            else:
                                rr_info.did_read_all_data = True
                        except BaseException as ie:
                            rr_info.last_exception = ie

                    reader = threading.Thread(target=read_next_chunk)
                    reader.start()
                    try:
                        reader.join(timeout=timeout)
                    finally:
                        if reader.is_alive():
                            print(
                                "Did not receive the next payload chunk of %r within %.3fs timeout. "
                                "Assuming the socket read operation is stuck",
                                url,
                                timeout,
                            )
                            raise FileIntegrityError()
                    if rr_info.did_read_all_data:
                        break
                    if rr_info.last_exception is not None:
                        raise rr_info.last_exception
 
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

