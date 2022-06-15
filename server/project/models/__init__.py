"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from dataclasses import dataclass

from fairreckitlib.recommender_system import RecommenderSystem

from .constants import MAIL_KEY, RESULTS_DIR
from .mail import MailSender
from .experiment_queue import ExperimentQueue
from .options_formatter import OptionsFormatter
from .result_storage import ResultStorage


@dataclass
class Token:
    """Contains the token for Spotify requests"""
    expiration_time: int
    token_type: str
    access_token: str


token = Token(0, '', '')

MAIL = {MAIL_KEY: None}


def make_mail(app):
    """Instantiate mail sender with app

    Args:
        app: the app to get the context from
    """
    MAIL[MAIL_KEY] = MailSender(app)


# Initialise
recommender_system = RecommenderSystem('datasets', RESULTS_DIR)
# TODO refactor
options_formatter = OptionsFormatter(recommender_system)
result_store = ResultStorage()
queue = ExperimentQueue(recommender_system,
                        options_formatter,
                        result_store,
                        MAIL)
