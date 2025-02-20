from flask import Flask, render_template, request, jsonify
from statsig import statsig, StatsigUser
import os
from dotenv import load_dotenv
import uuid 

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Statsig with your server SDK key
STATSIG_SERVER_KEY = os.getenv('STATSIG_SERVER_KEY')
statsig.initialize(STATSIG_SERVER_KEY)

@app.route('/')
def index():
    return render_template('ecommerce-site.html')

@app.route('/get-experiment-value')
def get_experiment_value():
    user_id = str(uuid.uuid4())
    user = StatsigUser(user_id)
    
    return jsonify({
        'buttonText': statsig.get_experiment(user, "button_text_variation").get("text_to_display", 'Add to Cart')
    })

@app.route('/log-event', methods=['POST'])
def log_event():
    try:
        data = request.json
        user_id = str(uuid.uuid4())
        user = StatsigUser(user_id)
        
        # Log the event to Statsig
        statsig.log_event(
            user=user,
            event_name=data.get('event_name', 'button_clicked'),
            value=None,
            metadata=data.get('metadata', {})
        )
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)