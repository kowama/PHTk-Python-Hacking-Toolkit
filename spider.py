#!/usr/bin/env python
import requests, argparse, re
import urlparse

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

def filter_links(links):
    fitered_links = []
    for link in links:
        link = urlparse.urljoin(TARGET, link)
        #filter
        if TARGET in link :
            if "#" in link :
                link = link.split("#")[0]
                
            if link not in fitered_links:
                fitered_links.append(link)

    return fitered_links

def get_resources(html):
    return re.findall(r'(?:src=")(.*?)"',html)

        
TARGET = get_arguments().target

page = request(TARGET)
links = get_links(page.content)
resources = get_resources(page.content)

print("\n===================Link============================")
flinks = filter_links(links)
for link in flinks:
    print(link)

print("\n===================SRC============================")
for src in resources:
    src = urlparse.urljoin(TARGET, src)
    print(src)
