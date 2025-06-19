from flask import Flask, request, render_template
from flask_httpauth import HTTPBasicAuth
import json
import os

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
        try:
            return json.load(f)
        except Exception:
            return []


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
    port = int(os.getenv('PORT', '5000'))
    app.run(host='0.0.0.0', port=port)
