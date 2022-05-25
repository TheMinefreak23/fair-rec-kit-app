
from flask import (Blueprint, request)
from flask_mail import Mail, Message

mail = {}

mail_bp = Blueprint('mail', __name__, url_prefix='/api/mail')


def make_mail(app):
    global mail
    mail = Mail(app)

def send_tweet()

@mail_bp.route('/test')
def index():
    msg = Message(subject = 'foobar',
                  body = 'I am calling to let you know about your cars expired warrenty please get back to me as soon as possible thanks :):):):)',
                  sender='foo@bar.gov',
                  recipients=['gaypiss6969@gmail.com'])
    mail.send(msg)
    #print(msg)
    return 'owo'

