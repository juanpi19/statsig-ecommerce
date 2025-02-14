from flask import Flask, render_template, jsonify, request, session
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Access the variables
api_key = os.getenv("secret_key")

@app.route('/')
def index():
    return render_template('ecommerce-site.html')

if __name__ == '__main__':
    app.run(debug=True)