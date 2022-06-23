"""This package contains all the models used to manipulate server data.

Modules:
    constants.py: This file contains constants that are used
    by the other classes (such as file paths)

    events.py: This file handles the events that are caused by the library,
    for example when an experiment is finished.

    experiment.py: This file defines different classes required to
    handle the progress of experiments and the experiment itself,
    which in turn has methods to run new experiments or validate them.

    experiment_queue.py: This module contains a class
    that handles the queueing of the experiments.

    mail.py: This module contains a class that is used to
    handle sending emails to the user whenever an experiment is finished.

    options_formatter.py: This contains a class and methods
    that are used to convert user experiment options
    to configuration dictionaries and vice-versa.

    result_loader.py: This module contains functions
    to load and modify data from evaluation results.

    result_storage.py: This module contains functions
    to load, save and modify data from the result overview.

classes:
    Token

methods:
    make_mail

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
    """Contains the token for Spotify requests."""

    expiration_time: int
    token_type: str
    access_token: str


token = Token(0, '', '')

MAIL = {MAIL_KEY: None}


def make_mail(app):
    """Instantiate mail sender with app.

    Args:
        app: the app to get the context from
    """
    MAIL[MAIL_KEY] = MailSender(app)


# Initialise
recommender_system = RecommenderSystem('datasets', RESULTS_DIR)
options_formatter = OptionsFormatter(recommender_system)
result_store = ResultStorage()
queue = ExperimentQueue(recommender_system,
                        options_formatter,
                        result_store,
                        MAIL)
