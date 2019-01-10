#!/usr/bin/env python

import optparse
import scapy.all as scapy

#user input
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="network", help="The target network to scan. examples:-n 192.168.1.0/24")
    options = parser.parse_args()[0]
    if not options.network :
        parser.error("[-] Please give network address, use --help for more info")
        exit()
    return  options

def scan(ip_addr):
    arp_req = scapy.ARP(pdst=ip_addr)#create ARP pacquet
    broadcast = scapy.Ether(dst="FF:FF:FF:FF:FF:FF")
    arp_broadcast_req = broadcast / arp_req
    answereds = scapy.srp(arp_broadcast_req, timeout=1, verbose=False)[0]
    clients = []
    for element in answereds :
        clients.append({"ip" : element[1].psrc,  "mac": element[1].hwsrc})
    return clients


options = get_arguments()
clients_list = scan(options.network)
#print the result
print("IP address \t\t mac-address\n-------------------------------------------------")
for client in clients_list :
    print(client["ip"]+ "\t\t"+ client["mac"])
