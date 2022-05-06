"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from flask import Flask
from flask_cors import CORS

from .computation import compute_bp
from .music_detail import detail_bp
from .result import result_bp
from .previous_results import results_bp
from .result_storage import create_results_overview


def create_app():
    """Instantiate the app."""
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

    register_blueprints(app)
    create_results_overview()
    return app


def register_blueprints(app):
    """
    Register Flask blueprints with routes.

    :param app: the main app
    """
    app.register_blueprint(compute_bp)
    app.register_blueprint(result_bp)
    app.register_blueprint(results_bp)
    app.register_blueprint(detail_bp)
