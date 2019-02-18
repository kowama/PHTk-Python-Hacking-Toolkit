#!/usr/bin/env python

import optparse
import scapy.all as scapy

#user input

def scan(ip_addr):
    arp_req = scapy.ARP(pdst=ip_addr)#create ARP pacquet
    broadcast = scapy.Ether(dst="FF:FF:FF:FF:FF:FF")
    arp_broadcast_req = broadcast / arp_req
    answereds = scapy.srp(arp_broadcast_req, timeout=1)[0]
    clients = []
    for element in answereds :
        clients.append({"ip" : element[1].psrc,  "mac": element[1].hwsrc})
    return clients


clients_list = []

string = "";
for i in range(0,256):
        print("IP RANGE  : 192.168."+ str(i) + ".0/24 ------------\n")
        clients_list  = scan("192.168."+ str(i) +".0/24")
        for client in clients_list :
            string +=  "[+] "+ client["ip"]+ "\t\t"+ client["mac"]+"\n"

#print the result
print("<=====================================================================>\n")
print("IP address \t\t mac-address\n=========================================")
print(string)
print("-----------------------------------------------------------")
      
