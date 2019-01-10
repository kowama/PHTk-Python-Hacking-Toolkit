#!/usr/bin/env python
import requests, re
import urlparse
from bs4 import BeautifulSoup


class Scanner:
    
    def __init__(self, url, links_to_ignore = []):
        self.target_url = url
        self.target_links = []
        self.links_to_ignore = links_to_ignore
        self.session = requests.session()

    def request(self, link):
        try:
            return self.session.get(link)
        except requests.ConnectionError:
            pass
        except Exception as err:
            print(err)
            pass

    def get_links(self, html):
        return re.findall(r'(?:href=")(.*?)"',html)

    def crawl(self,url=None):
        if url == None:
            url = self.target_links
        page = self.request(url)
        links = self.get_links(page.content)
        for link in links:
            link = urlparse.urljoin(url, link)

            #filter or TARGET
            if "#" in link :
                    link = link.split("#")[0]
            if self.target_url in link and link not in self.target_links and link not in self.links_to_ignore:
                    self.target_links.append(link)
                    print(" " +link)
                    self.crawl(link) 


    def map(self, verbose=True):
        if verbose:
            print("\n===================SITE-MAP============================")

        self.crawl(self.target_url)

        if verbose:
            print("===================FINISHED============================\n")      

    def extract_forms(self, link):
        page = self.session.get(link)
        parsed_html = BeautifulSoup(page.content,"html.parser")
        return parsed_html.find_all("form")

    def submit_form(self, form, dork, url):
        action = form.get("action")
        action_url = urlparse.urljoin(url, action)
        method = form.get("method")
        form_inputs = form.find_all("input")
        
        req_data={}
        for input in form_inputs:
            input_name = input.get("name")
            input_type = input.get("type")
            input_value = input.get("value")

            if input_type == "text":
                input_value = dork

            req_data[input_name] = input_value

        if method == "post":
            return self.session.post(action_url,data= req_data)
        else:
            return self.session.get(action_url, params=req_data)
    
    def run(self):
        for link in self.target_links:

            if "=" in link :
                print(" [+] Testing : " +link)
                #METHOD TO TEST SOME VULNE

            forms = self.extract_forms(link)
            for form in forms:
                print(" [+] Testing form in : "+link)
                #METHOD TO TEST SOME VULNE

