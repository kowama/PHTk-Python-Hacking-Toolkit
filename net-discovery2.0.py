#!/usr/bin/env python

import optparse
import scapy.all as scapy

#user input
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="network", help="The target network to scan. examples:-n 192.168.1.0/24")
    parser.add_option("-P", "--private", dest="private_range", help="Scan all the private IP range")
    (options, arguments) = parser.parse_args()
    if not options.network and not options.private_range:
        parser.error("[-] Please give network address, use --help for more info")
        exit()
    return  options

def scan(ip_addr):
    arp_req = scapy.ARP(pdst=ip_addr)#create ARP pacquet
    broadcast = scapy.Ether(dst="FF:FF:FF:FF:FF:FF")
    arp_broadcast_req = broadcast / arp_req
    (answereds, unanswereds) = scapy.srp(arp_broadcast_req, timeout=1)
    clients = []
    for element in answereds :
        clients.append({"ip" : element[1].psrc,  "mac": element[1].hwsrc})
    return clients


options = get_arguments()
clients_list = []
if(options.network):
    clients_list = scan(options.network)
    #print the result
    print("IP address \t\t mac-address\n--------------------")
    for client in clients_list :
        print("[+] "+ client["ip"] + "\t\t"+ client["mac"])

else:
    string = "";
    for i in range(0,256):
        for j in range(0, 256):
            print("IP RANGE  : 10."+ str(i)+"." + str(j) + ".0/24 ------------\n")
            clients_list  = scan("10."+ str(i) +"." + str(j) + ".0/24")
            for client in clients_list :
                string +=  "[+] "+ client["ip"]+ "\t\t"+ client["mac"]+"\n"

    #print the result
    print("<=====================================================================>\n")
    print("IP address \t\t mac-address\n=========================================")
    print(string)
    print("-----------------------------------------------------------")
      
