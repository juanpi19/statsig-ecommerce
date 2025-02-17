from flask import Flask, render_template, jsonify, request, session
from dotenv import load_dotenv
import os

load_dotenv() 
app = Flask(__name__)

@app.route('/')
def index():
    # statsig_key = os.environ.get('STATSIG_CLIENT_KEY', 'default_key')
    return render_template('ecommerce-site.html')

@app.route('/get-statsig-key')
def get_statsig_key():
    statsig_key = os.environ.get('STATSIG_CLIENT_KEY', 'default_key')
    return jsonify({'key': statsig_key})


if __name__ == '__main__':
    app.run(debug=True)