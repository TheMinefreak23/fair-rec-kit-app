"""This module tests the email sending functionality.

test_send_mail(): test the send_mail function.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from flask import Flask
from project.models import make_mail, MAIL, MAIL_KEY

app = Flask(__name__)
app.config['TESTING'] = True
make_mail(app)


def test_send_mail():
    """Test the send_mail function."""
    mail_sender = MAIL[MAIL_KEY]
    with mail_sender.mail.record_messages() as mailbox:
        mock_job = {'metadata': {'email': 'fake@email.com',
                                 'name': 'the final amogus'},
                    'timestamp': {'datetime': '2022-4-20 4:20:69'}}
        mail_sender.send_mail(mock_job)
        assert len(mailbox) == 1
        assert mailbox[0].body == 'Hello! \n' \
                                  'Your calculation with name ' \
                                  'the final amogus and datetime 2022-4-20 4:20:69 is done! \n\n' \
                                  'This is an automated e-mail.'
        assert mailbox[0].subject == 'Your calculation the final amogus is ready!'
        assert mailbox[0].recipients == ['fake@email.com']
        