import sys
from urllib import parse
import requests
from bs4 import BeautifulSoup


def path_strip(url):
    parser = parse.urlparse(url)
    return parser.scheme + '://' + parser.netloc


def extract_params(url):
    forms_list = []

    _html = requests.get(url).content
    bsoup = BeautifulSoup(_html, 'html.parser')
    forms = bsoup.find_all('form')

    for form in forms:
        form_data = {
        'url': '',
        'path': '',
        'method': '',
        'params': []
        }

        form_data['url'] = url
        form_data['path'] = form.attrs.get('action').lower()
        form_data['method'] = form.attrs.get('method').lower()
        for input_tag in form.find_all('input'):
            form_data['params'].append(input_tag.attrs.get('name'))

        forms_list.append(form_data)

    return forms_list


def scan(data):

    payload = '<svg/onload=alert("test XSS scanner")>'
    for form in data:
        if form['method'] == 'get':

            get_params = {

            }

            for param in form['params']:
                get_params[param] = payload
            response_body = requests.get(path_strip(form['url']) + form['path'], params=get_params)

            if payload in response_body.text:
                print(form['url'] + ' - vulnerable')

        elif form['method'] == 'post':
            print('POST method not supported')

filename = sys.argv[1]
with open(filename) as urls_list:
    urls = urls_list.readlines()
    for url in urls:
        scan(extract_params(url.strip()))

    