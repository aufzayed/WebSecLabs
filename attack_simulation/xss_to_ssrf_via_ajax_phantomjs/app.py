#!/usr/bin/python3

import os
from urllib import parse
from flask import *
from selenium import webdriver


vuln_app = Flask(__name__)

def download(driver, target_path):
    """Download the currently displayed page to target_path."""
    def execute(script, args):
        driver.execute('executePhantomScript',
                       {'script': script, 'args': args})

    # hack while the python interface lags
    driver.command_executor._commands['executePhantomScript'] = ('POST', '/session/$sessionId/phantom/execute')
    # set page format
    # inside the execution script, webpage is "this"
    page_format = 'this.paperSize = {format: "A4", orientation: "portrait" };'
    execute(page_format, [])

    # render current page
    render = '''this.render("{}")'''.format(target_path)
    execute(render, [])

def phantom_driver():
    driver = webdriver.PhantomJS('phantomjs')
    driver.get('file:///home/auf/env/AppSec/bug_reproduce/xss_to_ssrf_via_ajax_phantomjs/templates/export.html')
    download(driver, "save_me.pdf")



@vuln_app.route('/')
def home():
    return render_template('index.html')


@vuln_app.route('/image')
def load_image():
    image_id = request.args.get('id')
    try:
        return send_file(f'img/{image_id}', mimetype='image/jpg')
    except FileNotFoundError:
        return '<center><h1>Image Not Found</h1></center>', 404


@vuln_app.route('/login', methods=['GET', 'POST'])
def login():
    # credentials hardcoding is not a good idea
    username = 'admin'
    password = 'admin'

    if request.method.lower() == 'get':
        if request.cookies.get('logged'):
            if int(request.cookies.get('logged')):
                if request.cookies.get('username'):
                    if request.cookies.get('username') == username:
                        return redirect('/profile')
                    else:
                        return render_template('login.html')
                else:
                    return render_template('login.html')
            else:
                return render_template('login.html')
        else: 
            return render_template('login.html')

    elif request.method.lower() == 'post':
        uname = request.form.get('username')
        passwd = request.form.get('password')

        if uname == username and passwd == password:
            res = make_response(redirect('/profile'))
            res.set_cookie('logged', '1', 60*60*24)
            res.set_cookie('username', username, 60*60*24)
            return res
        elif uname == username and passwd != password:
            return render_template('login.html', error='Bad credentials')
        elif uname != username:
            return render_template('login.html', error='Bad credentials')


@vuln_app.route('/logout')
def logout():
    res = make_response(redirect('/login'))
    res.set_cookie('logged', '0', 60*60*24)
    res.set_cookie('username', '', 0)
    return res


@vuln_app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method.lower() == 'get':
        if request.cookies.get('logged'):
            if int(request.cookies.get('logged')):
                if request.cookies.get('username'):
                    return render_template('profile.html', username=request.cookies.get('username'))
                else:
                    return redirect('/login')
            else:
                return redirect('/login')
        else:
            return redirect('/login')
    elif request.method.lower() == 'post':
        bio = request.form.get('bio')
        print(bio)
        encode_bio = parse.quote(str(bio))
        print(encode_bio)
        return render_template('profile.html', username=request.cookies.get('username'), about=f'<p>{bio}</p>', pdf_export=f'<a href="export?bio={encode_bio}&username={request.cookies.get("username")}">Export profile as PDF</a>')


@vuln_app.route('/export')
def screenshot():
    template = '''
<html lang="en">
    <head>
    <meta charset="UTF-8">
    <title>export</title>
</head>
<body>
    <center>
        <h1>{{name}}</h1>
        <br>
        <br>
        <br>
        <h2>{{bio}}</h2>
    </center>
</body>
</html>
'''
    username = request.args.get('username')
    bio = request.args.get('bio')
    with open(f'temp/{username}.html', 'w') as temp_html:
        temp_html.write(template.replace('{{name}}', username).replace('{{bio}}', bio))

    driver = webdriver.PhantomJS('phantomjs')
    driver.get(os.path.abspath(f'temp/{username}.html'))
    download(driver, f"pdf/{username}.pdf")

    return send_file(f'pdf/{username}.pdf', mimetype='application/pdf')


if __name__ == "__main__":
    vuln_app.run(port=1337)