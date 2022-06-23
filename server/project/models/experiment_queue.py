"""This module contains a class that handles the queueing of the experiments.

classes:
    ExperimentQueue

methods:
    formatted_experiments

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
    """Queue for handling multiple experiments one by one.

    methods:
        __init__
        formatted_queue
        run_first
        set_up_experiment
        append_queue
        add_validation
        formatted_experiment
    """

    def __init__(self, recommender_system, options_formatter, result_storage, mail_sender):
        """Initialize ExperimentQueue.

        args:
            recommender_system(obj): the recommender system
            options_formatter(obj): options_formatter instance to be used
            result_storage(obj): result_storage instance to be used
            mail_sender(obj): mail_sender instance to be used
        """
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

    def set_up_experiment(self, experiment):
        """Set up an experiment before running it.

        Args:
            experiment(QueueItem): the experiment we are about to run

        Returns:
            experiment(dict) the experiment events
        """
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
        current_dt = now.strftime('%Y-%m-%d %H:%M:%S')
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
        experiment = Experiment(queue_item, self.recommender_system)
        self.filter_queue()
        self.queue.append(experiment)

    def add_validation(self, file_path, amount, result):
        """Add a validation experiment to the queue.

        Args:
            file_path(str): the path to the existing experiment result
            amount(int): the amount of runs for validation

        """
        result['file_path'] = file_path
        result['amount'] = amount
        queue_item = QueueItem(job = result,
                               config={},
                               name='',
                               status=Status.TODO,
                               progress=ProgressStatus.NA,
                               validating=True)
        experiment = Experiment(queue_item, self.recommender_system)
        self.filter_queue()
        self.queue.append(experiment)

    def filter_queue(self):
        """Filter out finished experiments when the queue is too long."""
        finished_experiments = len([
        item for item in self.queue
        if item.queue_item.status in (Status.DONE, Status.ABORTED)
    ])
        while finished_experiments > 5:
            self.queue.pop(0)
            finished_experiments -= 1

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
