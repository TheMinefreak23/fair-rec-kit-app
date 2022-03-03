from flask import Flask
from flask_cors import CORS

# Instantiate the app.
app = Flask(__name__)

# Enable CORS.
CORS(app)

CALCULATIONS = [
    {
        'timestamp': 'First',
        'author': 'Jack Kerouac',
    }
]

# Route: Do a sanity check.
@app.route('/greeting', methods=['GET'])
def greeting():
    return {"greeting": "Greetings from the backend :)"}

