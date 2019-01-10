#!/usr/bin/env python
#!/usr/bin/env python
import subprocess
import netfilterqueue

def process_pkt(pkt) :
   print(pkt)
   pkt.drop()

# put recieved packets in a queue Quenum=0
try : 
   subprocess.call("iptables -I FORWARD -jNFQUEUE --queue-num 0",shell=True)

   queue = netfilterqueue.NetfilterQueue()
   queue.bind(0, process_pkt)
   queue.run()

except KeyboardInterrupt:
   print("\n[-] Ctrl+C detected ....iptables flushed")
   #flush ip table to emmpty queue 0
   subprocess.call("iptables --flush",shell=True)
   print("[-] .....Quiting")

