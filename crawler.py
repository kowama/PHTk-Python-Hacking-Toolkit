#!/usr/bin/env python
import requests, argparse

SUBDOMAINS_LIST="subdomains.list"
PATHS_LIST = "paths.list"


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="The target : example.com")
    args = parser.parse_args()
    if not args.target:
        parser.error("[-] Please give target  address, use --help for more info")
        exit()
    return args


def request(link):
    try:
        return requests.get(link)
    except requests.ConnectionError:
        pass
    except Exception as err:
        print(err)
        pass


def discover_subdomain(TARGET):
    with open(SUBDOMAINS_LIST,"r") as word_list:
        for line in word_list:
            sub = line.strip()
            link = "http://"+sub + "." + TARGET
            resp = request(link)
            if resp:
                print("[+] Discovered subdomain at --> "+link)


def discover_path(TARGET):
    with open(PATHS_LIST, "r") as word_list:
        for line in word_list:
            path = line.strip()
            link = "http://"+ TARGET+"/"+path
            resp = request(link)
            if resp:
                print("[+] Discovered URL at --> "+link)
        
TARGET = get_arguments().target

print("\n===================SUB-DOMAINS====================")
discover_subdomain(TARGET)
print("\n=======================URL========================")
discover_path(TARGET)