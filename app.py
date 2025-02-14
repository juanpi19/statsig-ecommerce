from flask import Flask, render_template, jsonify, request, session
from dotenv import load_dotenv
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('ecommerce-site.html')

if __name__ == '__main__':
    app.run(debug=True)