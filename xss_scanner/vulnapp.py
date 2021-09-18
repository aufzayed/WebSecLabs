#!/user/bin/python3

import html
from types import resolve_bases
from flask import *


vulnapp = Flask(__name__)



@vulnapp.route('/')
def home():
    response_body = """<!DOCTYPE html>
<html>
    <head>
        <title>vuln app</title>
    </head>
    <body>
        <center><h1>Welcom To VulnApp</h1></center>
        <br>
        <br>
        <center>
            <ul>
                <li><a href="/vuln_echo?name=@aufzayed">vuln echo</a></li>
                <li><a href="/secure_echo?name=@aufzayed">secure echo</a></li>
                <li><a href="/vuln_form_echo">vuln form</a></li>
            </ul>
        </center>
    </body>
</html>
    """
    return response_body

@vulnapp.route('/vuln_echo')
def vuln_echo():
    response_body = """<!DOCTYPE html>
<html>
    <head>
        <title>vuln app</title>
    </head>
    <body>
        <center><h1>Welcom To VulnApp</h1></center>
        <br>
        <br>
        <center><h2>Hello, <name></h2></center>
    </body>
</html>
    """
    username = request.args.get('name')
    return response_body.replace('<name>', username)

@vulnapp.route('/vuln_form_echo')
def vuln_form_echo():
    response_body = """<!DOCTYPE html>
<html>
    <head>
        <title>vuln app</title>
    </head>
    <body>
        <center><h1>Welcom To VulnApp</h1></center>
        <br>
        <br>
        <center>
        <form action='/vuln_form_echo' method='GET'>
            <input type='text' name='name'>
            <button type='submit'>print your name</button>
        </form>
        </center>
        <br>
        <br>
        <center><h2>Hello, <name></h2></center>
    </body>
</html>
    """
    
    username = request.args.get('name')
    if username:
        return response_body.replace('<name>', username)
    else:
        return response_body.replace('<center><h2>Hello, <name></h2></center>', '')
@vulnapp.route('/secure_echo')
def secure_echo():
    response_body = """<!DOCTYPE html>
<html>
    <head>
        <title>secure app</title>
    </head>
    <body>
        <center><h1>Welcom To Secure App</h1></center>
        <br>
        <br>
        <center><h2>Hello, <name></h2></center>
    </body>
</html>
    """
    username = request.args.get('name')
    return response_body.replace('<name>', html.escape(username))

if __name__ == '__main__':
    vulnapp.run(port=1337)