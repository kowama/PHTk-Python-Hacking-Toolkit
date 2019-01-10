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
            url = self.target_url
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
    
    def check_xss(self, form, link):
        xss_text_script='<scriPt>alert("hello world !")</sCript>'
        resp = self.submit_form(form, xss_text_script, link)
        if xss_text_script in resp.content:
            return True
        else:
            return False

    def login(self, url, payload, login_detect={'username':["username","user","email"], 'password':["password", "passwd", "pass"]}):
        forms = self.extract_forms(url)
        login_form = None
        for form in forms :
            for word in ["log", "auth"]:
                if word in form.get("action"):
                    login_form = form
                    break
            if login_form is not None:
                break

        if login_form is not None:
            action = login_form.get("action")
            action_url = urlparse.urljoin(url, action)
            lform_inputs = login_form.find_all("input")
            
            req_data={}
            for input in lform_inputs:
                input_name = input.get("name")
                input_value = input.get("value")

                if input_name in login_detect['username']:
                    req_data[input_name] = payload['username']
                
                elif input_name in login_detect['password']:
                    req_data[input_name] = payload['password']

                else:
                    req_data[input_name] = input_value

            print(req_data)
            return self.session.post(action_url,data= req_data)
        else:
            print("[-] login form not find") 
            return None


        def run(self):
            for link in self.target_links:

                if "=" in link :
                    print(" [+] Testing : " +link)
                    #METHOD TO TEST SOME VULNE
                

                forms = self.extract_forms(link)
                for form in forms:
                    print(" [+] Testing form in : "+link)
                    #METHOD TO TEST SOME VULNE
                    if self.check_xss(form,link):
                        print("[*] ****XSSS vunlnerability at form "+link)

