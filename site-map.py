#!/usr/bin/env python
import requests, argparse, re
import urlparse

site_links = []


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="The target : http://example.com")
    args = parser.parse_args()
    if not args.target:
        parser.error("[-] Please give target  http://example.com, use --help for more info")
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

def get_links(html):
    return re.findall(r'(?:href=")(.*?)"',html)

def crawl(url):
    page = request(url)
    links = get_links(page.content)
    for link in links:
        link = urlparse.urljoin(url, link)
        #filter or TARGET
        if url in link :
            if "#" in link :
                link = link.split("#")[0]
                
            if link not in site_links:
                site_links.append(link)
                print(" " +link)
                crawl(link)           

TARGET = get_arguments().target
print("\n===================SITE-MAP============================")

try:
   crawl(TARGET)
except KeyboardInterrupt:
    print("Ctrl+C detected ....Quiting")