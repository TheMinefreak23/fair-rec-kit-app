"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import base64

import requests as requests
from flask import Flask
from flask_cors import CORS

from project.computation import compute_bp
from project.previous_results import results_bp
from project.result_storage import create_results_overview


def create_app(test_config=None):
    # Instantiate the app.
    app = Flask(__name__)
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.config['TESTING'] = True

    # Enable Cross-Origin Resource Sharing.
    CORS(app)

    # Route: Main.
    @app.route('/api', methods=['GET'])
    def main():
        return {"msg": "Server online."}

    # Route: Do a sanity check.
    @app.route('/api/greeting', methods=['GET'])
    def greet():
        return {"greeting": "Greetings from the backend :)"}

    # Route: Spotify token.
    @app.route('/api/token', methods=['GET'])
    def token():
        id = '7e49545dfb45473cbe595d8bb1e22071'
        secret = 'd5a9e8febef2468b94a5edabe2c5ddeb'
        message = (id + ':' + secret).encode()
        encoded = base64.b64encode(message)
        print('encoded',encoded)
        headers = {'Authorization': 'Basic ' + encoded.decode()
                   ,'Content-Type': 'application/x-www-form-urlencoded'}
        data = 'grant_type=client_credentials'
        res = requests.post('https://accounts.spotify.com/api/token', data=data, headers=headers)
        print(res.text)
        return res.text

    register_blueprints(app)
    create_results_overview()
    return app


def register_blueprints(app):
    app.register_blueprint(compute_bp)
    app.register_blueprint(results_bp)
