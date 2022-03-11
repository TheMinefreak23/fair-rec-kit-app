#This program has been developed by students from the bachelor Computer Science at
#Utrecht University within the Software Project course.
#© Copyright Utrecht University (Department of Information and Computing Sciences)
import os

from flask import Flask, request
from flask_cors import CORS

from . import computation

def create_app(test_config=None):
    # Instantiate the app.
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
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

    # Route: Do a sanity check.
    @app.route('/greeting', methods=['GET'])
    def greet():
        return {"greeting": "Greetings from the backend :)"}

    app.register_blueprint(computation.bp)
    return app

