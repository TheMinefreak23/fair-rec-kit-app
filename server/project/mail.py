
from flask import (Blueprint, request)
from flask_mail import Mail, Message

mail = {}
mail_app = {}
mail_bp = Blueprint('mail', __name__, url_prefix='/api/mail')


def make_mail(app):
    global mail
    global mail_app
    mail_app = app
    mail = Mail(app)


def send_mail(adress, name, timestamp):
    global mail
    msg = Message(subject='Your calculation ' + name + ' is ready!',
            body='Hello! \n Your calculation with name ' + name + ' and timestamp ' + timestamp + " is done!",
            sender='fairreckit@noreply.com',
            recipients=[adress])
    with mail_app.app_context():
        mail.send(msg)

@mail_bp.route('/test')
def index():
    msg = Message(subject = 'foobar',
                  body = 'I am calling to let you know about your cars expired warrenty please get back to me as soon as possible thanks :):):):)',
                  sender='foo@bar.gov',
                  recipients=['voswesseling@gmail.com'])
    mail.send(msg)
    #print(msg)
    return 'owo'


# TODO Is this a mock?
def send_email(metadata, timestamp):
    print("llanfairpwlchfairgwyngychgogerychchwryrndrwbwchllantisiligogogoch")
    print(metadata["name"])
    print(metadata["email"])
    print(timestamp)

