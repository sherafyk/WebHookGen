
### Task 1: Initialize the GitHub Repo & Project Structure

1. **Create and clone repo**

   ```bash
   git clone https://github.com/sherafyk/WebHookGen.git
   cd WebHookGen
   ```
2. **Create directories and files**

   ```
   WebHookGen/
   ├── app/
   │   ├── main.py
   │   ├── data.json          ← start as empty array: []
   │   └── templates/
   │       └── index.html
   ├── requirements.txt
   ├── Dockerfile
   └── README.md
   ```
3. **Initialize files**

   * `data.json`: add `[]`
   * `README.md`: note repo purpose and “Usage” summary

---

### Task 2: Implement the Flask Webhook App

1. **requirements.txt**

   ```
   flask
   flask_httpauth
   ```
2. **app/main.py**

   ```python
   from flask import Flask, request, render_template
   from flask_httpauth import HTTPBasicAuth
   import json, os

   app = Flask(__name__)
   app.secret_key = 'letterly-webhook-secret'
   auth = HTTPBasicAuth()

   USERNAME = 'admin'
   PASSWORD = os.getenv('WEBHOOK_PASS', 'AppPass1')
   DATA_FILE = 'data.json'

   def load_data():
       if not os.path.exists(DATA_FILE):
           return []
       with open(DATA_FILE) as f:
           try: return json.load(f)
           except: return []

   def save_data(items):
       with open(DATA_FILE, 'w') as f:
           json.dump(items, f, indent=2)

   @auth.verify_password
   def verify(u, p):
       return u == USERNAME and p == PASSWORD

   @app.route('/', methods=['GET'])
   @auth.login_required
   def home():
       return render_template('index.html', items=load_data())

   @app.route('/webhook', methods=['POST'])
   def webhook():
       data = request.get_json() or request.form.to_dict()
       items = load_data()
       items.insert(0, data)
       save_data(items)
       return {'status': 'received'}, 200

   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=5000)
   ```
3. **app/templates/index.html**

   ```html
   <!DOCTYPE html>
   <html>
   <head>
     <meta charset="utf-8">
     <title>Webhook Submissions</title>
     <style>
       body { font-family:sans-serif; background:#f7f7f7; margin:0; }
       .container { max-width:800px; margin:40px auto; }
       .card { background:#fff; margin:1em 0; padding:1.5em; border-radius:10px; box-shadow:0 2px 6px rgba(0,0,0,0.1); }
       pre { white-space:pre-wrap; word-break:break-all; }
       h1 { text-align:center; color:#444; }
     </style>
   </head>
   <body>
     <div class="container">
       <h1>Webhook Submissions</h1>
       {% if items %}
         {% for item in items %}
           <div class="card"><pre>{{ item|tojson(indent=2) }}</pre></div>
         {% endfor %}
       {% else %}
         <p>No webhook submissions yet.</p>
       {% endif %}
     </div>
   </body>
   </html>
   ```

---

### Task 3: Dockerize the App

1. **Dockerfile** (at repo root)

   ```Dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY app/ /app
   EXPOSE 5000
   CMD ["python", "main.py"]
   ```
2. **Build & Run**

   ```bash
   # Build
   docker build -t webhook-gen .

   # Run (mount data.json so submissions persist)
   docker run -d \
     --name webhook-gen \
     -e WEBHOOK_PASS=AppPass1 \
     -p 5000:5000 \
     -v "$PWD/app/data.json":/app/data.json \
     webhook-gen
   ```

   3. Review all code and edit the README.md file to be a comprehensive documentation of the code, with clear instructions at the top.

---

### Task 4: Deploy Behind Apache & Configure Letterly

1. **Enable Apache proxy modules**

   ```bash
   sudo a2enmod proxy proxy_http
   sudo systemctl restart apache2
   ```
2. **VirtualHost for `sub.domain.com`**

   ```apache
   <VirtualHost *:80>
     ServerName sub.domain.com

     ProxyPreserveHost On
     ProxyPass        / http://127.0.0.1:5000/
     ProxyPassReverse / http://127.0.0.1:5000/
   </VirtualHost>
   ```
3. **Reload Apache**

   ```bash
   sudo systemctl reload apache2
   ```
4. **Set Letterly webhook URL**

   ```
   https://sub.domain.com/webhook
   ```

---


