# server-side request forgery (SSRF) labs


## install
 
 ```
 python3 -m pip install requests flask pdfkit
 sudo apt-get install wkhtmltopdf
 ```
 
 ## run
 ```
 cd ssrf
 python3 app.py
 python3 internal_service/monitor.py
```

app.py -> http://localhost:1337/
monitor.py -> http://localhost:13337/
