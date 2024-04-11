#!/usr/bin/env python

import time
import os
import six
from six.moves import range
from six.moves.http_client import BadStatusLine, IncompleteRead
from six.moves.urllib_error import HTTPError, URLError
from six.moves.urllib_parse import urlparse
from six.moves.urllib_request import Request, urlopen

import zipfile
import os
import shutil
import subprocess


def extract_zip(zip_file_path, target_folder):
    print('extract')
    # Ensure target_folder exists
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # Construct the unzip command
    command = ["unzip", "-o", "-q", zip_file_path, "-d", target_folder]

    # Execute the command
    try:
        subprocess.check_call(command)
        print("ZIP file extracted successfully")
    except subprocess.CalledProcessError as e:
        print("Failed to extract ZIP file")
    

def download_and_unzip_zip(url, target_folder):
    print('download')
    # Define the path for the temporary downloaded ZIP file
    req = Request(url)
    
    temp_zip_path = os.path.join(target_folder, url.split('/')[-1])
    # Download the ZIP file
    response = urlopen(req)
    out_file = open(temp_zip_path, 'wb')
    shutil.copyfileobj(response, out_file)
    time.sleep(60)

    extract_zip(temp_zip_path, target_folder)


url = "https://storage.googleapis.com/sauce-devx-runners-bhtb/cypress-macos-amd64-8622143467.zip"
result = download_and_unzip_zip(url, './')
print(result)

