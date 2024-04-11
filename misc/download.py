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
import hashlib

timeout = 1

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
    
    print('size: ', os.path.getsize(zip_file_path))

def download_and_unzip_zip(url, target_folder):
    print('download')
    # Define the path for the temporary downloaded ZIP file
    req = Request(url)
    
    zip_path = os.path.join(target_folder, url.split('/')[-1])
    # Download the ZIP file
    response = urlopen(req, timeout=timeout)
    out_buffer = open(zip_path, 'wb')
    shutil.copyfileobj(response, out_buffer)
    size = os.path.getsize(zip_path)
    print('size: ', size)
    md5 = hashlib.md5(open(zip_path,'rb').read()).hexdigest()
    print('md5: ', md5)
    #time.sleep(60)

    extract_zip(zip_path, target_folder)


url = "https://storage.googleapis.com/sauce-devx-runners-bhtb/cypress-macos-amd64-8622143467.zip"
result = download_and_unzip_zip(url, './')
print(result)

