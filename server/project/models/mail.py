"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from flask_mail import Mail, Message


class MailSender:
    """Send a mail when an experiment is done"""

    def __init__(self, app):
        self.app = app
        self.mail = Mail(app)

    def send_mail(self, address, name, timestamp):
        """Sends an e-mail to notify the user their experiment is done.

        Keyword arguments:
        adress      -- the adress the e-mail will be sent to
        name        -- the name of the experiment
        timestamp   -- the timestamp of when the experiment was started
        """
        msg = Message(subject='Your calculation ' + name + ' is ready!',
                      body='Hello! \nYour calculation with name ' + name
                           + ' and timestamp ' + timestamp
                           + ' is done! \n\nThis is an automated e-mail.',
                      sender='fairreckit@noreply.com',
                      recipients=[address])
        with self.app.app_context():
            self.mail.send(msg)

    # TODO
    @staticmethod
    def do_nothing():
        """This function exists to quit pylint from yappin"""
        return None
