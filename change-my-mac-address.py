#!/usr/bin/env python
import subprocess # execute system commande
import optparse #read user agrs
import re # allow us to use reg expr

#user input
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change it mac-address")
    parser.add_option("-m", "--mac-address", dest="mac_addr", help="New mac-address to give to the interface")
    options = parser.parse_args()[0]
    if not options.interface :
        parser.error("[-] Please give the interface name, use --help for more info")
    if not options.mac_addr :
        parser.error("[-] Please give the new mac-address, use --help for more info")
    return  options

#mac_address changer function
def change_mac(interface, mac_addr):
    print("[+] Changing mac-address for " + interface + " to "+ mac_addr)
    subprocess.call("ifconfig " + interface + " down", shell = True)
    subprocess.call("ifconfig "+ interface + " hw ether "+ mac_addr,shell = True )
    subprocess.call("ifconfig " + interface + " up", shell = True)

#check if mac address is changed
def get_mac_address(interface):
    output = subprocess.check_output(["ifconfig", interface])
    mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", output).group(0)
    return mac

options = get_arguments()
print("[!] Current mac-address : " + str(get_mac_address(options.interface)))
change_mac(options.interface, options.mac_addr)
if(get_mac_address(options.interface) == options.mac_addr):
    print("[+] All work fine mac-address changed to " + str(get_mac_address(options.interface)))
else:
    print("[-] Something got wrong ! mac-address didn't changed " + str(get_mac_address(options.interface)))
