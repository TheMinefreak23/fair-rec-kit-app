"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

import time
from datetime import datetime

from .constants import MAIL_KEY
from .events import EventHandler
from .experiment import Status, ProgressStatus, QueueItem, Experiment


class ExperimentQueue:
    """Queue for handling multiple experiments one by one"""
    def __init__(self, recommender_system, options_formatter, result_storage, mail_sender):
        self.options_formatter = options_formatter
        self.recommender_system = recommender_system
        self.result_storage = result_storage
        self.mail_sender = mail_sender

        self.queue = []
        self.current_experiment = None

    def formatted_queue(self):
        """Format the queue to a list of formatted experiments (dictionaries).

        Returns:
            (list(dict)) the list of formatted experiments

        """
        # Format queue to dict list
        return [formatted_experiment(experiment) for experiment in self.queue]

    def run_first(self):
        """Take the oldest settings in the queue and perform an experiment with them."""

        # Do one experiment at a time
        if self.current_experiment and self.current_experiment.queue_item.status == Status.ACTIVE:
            return

        # Get the oldest experiment from the queue.
        # experiment = experiment_queue.pop()

        # Get the oldest experiment from the queue that is marked to do.
        first = next(filter(lambda item: item.queue_item.status == Status.TODO, self.queue), None)

        # If there is a queue item to do, run it.
        # Either start a validation of an existing result or run a new experiment.
        if first:
            events = self.set_up_experiment(first)
            if first.queue_item.validating:
                self.current_experiment.validate_experiment(events)
            else:
                self.current_experiment.run_new_experiment(events)
            # mock_experiment(experiment)

    def set_up_experiment(self, experiment):
        """Set up an experiment before running it.

        Args:
            experiment(QueueItem): the experiment we are about to run

        Returns:
            experiment(dict) the experiment events
        """

        # print('run experiment:', experiment)

        # Update current experiment
        self.current_experiment = experiment

        # Make a new event handler and get experiment events
        return EventHandler(self.current_experiment.queue_item,
                            self.result_storage,
                            self.mail_sender[MAIL_KEY]).events

    def append_queue(self, metadata, settings):
        """Add a regular/new experiment item (settings) to the queue.

        Args:
            metadata(dict): the experiment metadata
            settings(dict): the experiment settings
        """
        # Handle empty name
        if 'name' not in metadata:
            metadata['name'] = 'Untitled'

        # Set time
        timestamp = time.time()
        now = datetime.now()
        current_dt = now.strftime('%Y-%m-%d %H:%M:%S')  # + ('-%02d' % (now.microsecond / 10000))
        job = {'timestamp': {'stamp': str(int(timestamp)),
                             'datetime': current_dt},
               'metadata': metadata,
               'settings': settings}

        # Create configuration dictionary.
        config_dict, config_id = self.options_formatter.config_dict_from_settings(job)

        # TODO refactor job and config_dict overlap
        queue_item = QueueItem(job,
                                config_dict,
                                Status.TODO,
                                ProgressStatus.NA,
                                config_id)
        current_job = Experiment(queue_item, self.recommender_system)

        self.queue.append(current_job)

    def add_validation(self, file_path, amount):
        """Add a validation experiment to the queue.

        Args:
            file_path(str): the path to the existing experiment result
            amount(int): the amount of runs for validation

        """
        experiment = QueueItem(job={'file_path': file_path, 'amount': amount},
                               config={},
                               name='',
                               status=Status.TODO,
                               progress=ProgressStatus.NA,
                               validating=True)
        self.queue.append(experiment)
        self.run_first()


def formatted_experiment(experiment):
    """Format the experiment to a dictionary.

    Args:
        experiment(QueueItem): the experiment from the queue

    Returns:
        (dict) the formatted experiment

    """
    if not experiment:
        return {}
    return experiment.to_dict()

