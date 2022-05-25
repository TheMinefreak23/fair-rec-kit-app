"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from flask import Flask
from flask_cors import CORS
from flask_mail import Mail, Message

from .experiment import compute_bp
from .music_detail import detail_bp
#from .result import result_bp
from .previous_results import results_bp
from .result_storage import create_results_overview


def create_app():
    """Instantiate the app."""
    app = Flask(__name__)
    app.config['ENV'] = 'development'
    app.config['DEBUG'] = True
    app.config['TESTING'] = False

    # Mail stuff
    app.config['MAIL_SERVER']='smtp.mailtrap.io'
    app.config['MAIL_PORT'] = 2525
    app.config['MAIL_USERNAME'] = '54587a9324d744'
    app.config['MAIL_PASSWORD'] = '0da1c03c71700d'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    # app.config['MAIL_SUPRESS_SEND'] = False
    mail = Mail(app)
    
    @app.route('/mail')
    def index():
        msg = Message(subject = 'foobar',
                      body = 'I am calling to let you know about your cars expired warrenty please get back to me as soon as possible thanks :):):):)',
                      sender='foo@bar.gov',
                      recipients=['gaypiss6969@gmail.com'])
        mail.send(msg)
        #print(msg)
        return 'owo'

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
    #app.register_blueprint(result_bp)
    app.register_blueprint(results_bp)
    app.register_blueprint(detail_bp)
