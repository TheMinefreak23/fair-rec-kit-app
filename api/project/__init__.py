# This program has been developed by students from the bachelor Computer Science at
# Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
import os

from flask import Flask
from flask_cors import CORS

from project.computation import compute_bp
from project.previous_results import results_bp


def create_app(test_config=None):
    # Instantiate the app.
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # Get the folder of the top-level directory of this project
        BASEDIR=os.path.abspath(os.path.dirname(__file__))
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

        # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Enable Cross-Origin Resource Sharing.
    CORS(app)

    # Route: Main.
    @app.route('/', methods=['GET'])
    def main():
        return {"msg": "Server online."}

    # Route: Do a sanity check.
    @app.route('/greeting', methods=['GET'])
    def greet():
        return {"greeting": "Greetings from the backend :)"}

    register_blueprints(app)
    return app


def register_blueprints(app):
    app.register_blueprint(compute_bp)
    app.register_blueprint(results_bp)
