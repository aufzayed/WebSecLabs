#!/usr/bin/env python3
import sys
from urllib import parse
import requests

def qs_replace(url):
    parser = parse.urlparse(url)

    # split query string
    _split = [i.split('=') for i in parser.query.split('&')]

    # replace parameters values with 'XSS' string
    for i in range(len(_split)):
        _split[i][1] = 'XSS'
    
    # join parameters list to creat new query string
    _query = '&'.join(['='.join(a) for a in _split])


    
    return parser.scheme + '://' + parser.netloc + parser.path + '?' + _query
    

def scan(url):
    payload = '<svg/onload=alert("Test XSS scanner)'
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
        scan(qs_replace(url.strip()))