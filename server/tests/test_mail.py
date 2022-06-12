"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from flask import Flask
from project.models.mail import _M, make_mail, send_mail

app = Flask(__name__)
app.config['TESTING'] = True
make_mail(app)

def test_send_mail():
    """Testing the send_mail function"""
    with _M['MAIL'].record_messages() as mailbox:
        send_mail('fake@email.com', 'the final amogus', '2022-4-20 4:20:69')
        assert len(mailbox) == 1
        assert mailbox[0].body == 'Hello! \nYour calculation with name the final amogus and timestamp 2022-4-20 4:20:69 is done! \n\nThis is an automated e-mail.'
        assert mailbox[0].subject == 'Your calculation the final amogus is ready!'
        assert mailbox[0].recipients == ['fake@email.com']
        