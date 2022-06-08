"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from typing import Any
from flask import Blueprint
from flask_mail import Mail, Message

_M = {'MAIL': Any}
_MA = {'MAIL_APP': Any}
mail_bp = Blueprint('mail', __name__, url_prefix='/api/mail')

def make_mail(app):
    """Instanciate the MAIL and the MAIL_APP"""
    _MA['MAIL_APP'] = app
    _M['MAIL'] = Mail(app)


def send_mail(adress, name, timestamp):
    """Sends an e-mail to notify the user their experiment is done.

    Keyword arguments:
    adress      -- the adress the e-mail will be sent to
    name        -- the name of the experiment
    timestamp   -- the timestamp of when the experiment was started
    """
    msg = Message(subject='Your calculation ' + name + ' is ready!',
            body='Hello! \nYour calculation with name ' + name
            + ' and timestamp ' + timestamp + ' is done! \n\nThis is an automated e-mail.',
            sender='fairreckit@noreply.com',
            recipients=[adress])
    with _MA['MAIL_APP'].app_context():
        _M['MAIL'].send(msg)

@mail_bp.route('/test')
def index():
    """TODO remove this"""
    msg = Message(subject = 'foobar',
                  body = 'this is a test',
                  sender='foo@bar.gov',
                  recipients=['voswesseling@gmail.com'])
    _M['MAIL'].send(msg)
    return 'owo'
