#!/usr/bin/env python3
import time
import json
from urllib.parse import urlparse
import pdfkit
import requests
from flask import *


app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/lab1', methods=['GET', 'POST'])
def lab1():
    if request.method == 'GET':
        return render_template('lab1.html')
    elif request.method == 'POST':
        try:
            image_url = request.form.get('image_url')
            image_name = url_to_name(image_url)
            res = requests.get(image_url)
            with open(f'images/{image_name}', 'wb') as save_image:
                save_image.write(res.content)
            return render_template('lab1.html', result=f'/load_image?name={image_name}')
        except Exception as e:
            return render_template('lab1.html', error=e)


@app.route('/lab2', methods=['GET', 'POST'])
def lab2():
    if request.method == 'GET':
        return render_template('lab2.html')
    elif request.method == 'POST':
        site_url = request.form.get('site_url')
        try:
            res = requests.get(site_url)
            return render_template('lab2.html', result=f'The website is working [{res.status_code}]')
        except Exception as e:
            return render_template('lab2.html', error=e)



@app.route('/lab3', methods=['GET', 'POST'])
def lab3():
    if request.method == 'GET':
        return render_template('lab3.html')
    elif request.method == 'POST':
        user_data = {}
        user_data['username'] = request.form.get('username')
        user_data['discription'] = request.form.get('discription')
        with open(f'db/{user_data["username"]}.json', 'w') as save_to_db:
            save_to_db.write(json.dumps(user_data))
        return redirect(f'/profile?username={request.form.get("username")}')


@app.route('/profile')
def profile():
    if request.query_string:
        params = request.query_string.decode('utf-8').split('&')

        if len(params) == 2:
            username = params[0].split('=')[1]
            to_pdf = params[1].split('=')[1]
            if to_pdf:
                with open(f'db/{username}.json') as user_data:
                    data = json.load(user_data)
                    pdfkit.from_string(
                        render_template('profile.html', username=data['username'], discription=data['discription']),
                        f'pdf/{username}.pdf'
                        )
                    return send_file(f'pdf/{username}.pdf', mimetype=('application/pdf'))
            else:
                return redirect(f'/profile?username={username}')

        elif len(params) == 1:
            username = params[0].split('=')[1]
            try:
                with open(f'db/{username}.json') as user_data:
                    data = json.load(user_data)
                    return render_template('profile.html', username=data['username'], discription=data['discription'])
            except FileNotFoundError:
                return redirect('/lab3')
    else:
        return redirect('/lab3') 

@app.route('/load_image')
def image():
    q = request.query_string.decode('utf-8').split('=')
    i_name = q[1]
    print(i_name)
    return send_file(f'images/{i_name}', mimetype=(f'image/{i_name.split(".")[1]}'))


def url_to_name(url):
    name = urlparse(url).path.split('/')[-1]
    if name == '':
        return f'{str(int(time.time()))}.unknown'
    else:
        return name


if __name__ == "__main__":
    app.run(port=1337)
