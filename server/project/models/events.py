"""This file handles the events that are caused by the library, for example when an experiment is finished.

classes:
    EventHandler

methods:
    do_nothing

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""

from fairreckitlib.experiment.experiment_event import \
    ON_END_EXPERIMENT_THREAD, ON_BEGIN_EXPERIMENT_THREAD
from fairreckitlib.model.pipeline.model_event import ON_BEGIN_MODEL_PIPELINE, \
    ON_BEGIN_TRAIN_MODEL, ON_BEGIN_LOAD_TRAIN_SET
from fairreckitlib.data.pipeline.data_event import ON_BEGIN_DATA_PIPELINE, \
    ON_BEGIN_FILTER_DATASET, ON_BEGIN_SPLIT_DATASET
from fairreckitlib.core.parsing.parse_event import ON_PARSE
from .experiment import Status, ProgressStatus


class EventHandler:
    """Handle the events.

    methods:
        __init__
        handle_event
        on_begin_experiment_thread
        on_end_experiment_thread
    """

    def __init__(self, experiment, result_storage, mail_sender):
        """Initialize an instance of EventHandler.

        args:
            experiment(obj): the experiment that will have its events handled.
            result_storage(obj): the current result_storage instance being used.
            mail_sender(obj): the current mail sender instance being used.
        """
        self.experiment = experiment
        self.result_storage = result_storage
        self.mail_sender = mail_sender
        event_ids = [
            ON_BEGIN_EXPERIMENT_THREAD,
            ON_END_EXPERIMENT_THREAD,
            # ON_PARSE, TODO doesn't work in Lib?
            ON_BEGIN_DATA_PIPELINE,
            ON_BEGIN_FILTER_DATASET,
            ON_BEGIN_SPLIT_DATASET,
            ON_BEGIN_MODEL_PIPELINE,
            ON_BEGIN_LOAD_TRAIN_SET,
            ON_BEGIN_TRAIN_MODEL,
        ]
        self.events = {event_id : self.handle_event for event_id in event_ids}

    def handle_event(self, event_listener, event_args, **kwargs):
        """Handle the event based on its ID.

        args:
            event_listener(obj): the event_listener to be used
            event_args(dict): the event arguments
        """
        do_nothing(event_listener, kwargs)

        progress_dict = {
            ON_PARSE: ProgressStatus.PARSING,
            ON_BEGIN_DATA_PIPELINE: ProgressStatus.PROCESSING_DATA,
            ON_BEGIN_FILTER_DATASET: ProgressStatus.FILTERING_DATA,
            ON_BEGIN_SPLIT_DATASET: ProgressStatus.SPLITTING_DATA,
            ON_BEGIN_MODEL_PIPELINE: ProgressStatus.MODEL,
            ON_BEGIN_LOAD_TRAIN_SET: ProgressStatus.MODEL_LOAD,
            ON_BEGIN_TRAIN_MODEL: ProgressStatus.TRAINING
        }

        if event_args.event_id == ON_BEGIN_EXPERIMENT_THREAD:
            self.on_begin_experiment_thread()
        elif event_args.event_id == ON_END_EXPERIMENT_THREAD:
            self.on_end_experiment_thread()
        else:
            """Change progress status."""
            self.experiment.progress = progress_dict[event_args.event_id]

    def on_begin_experiment_thread(self):
        """Change progress status to started and update the experiment status to active."""
        self.experiment.status = Status.ACTIVE
        self.experiment.progress = ProgressStatus.STARTED

    def on_end_experiment_thread(self):
        """Change progress status to finished and experiment status to "done".

        Also sends an email if possible.
        """
        if self.experiment.status is not Status.ABORTED:
            if not self.experiment.validating:
                self.result_storage.save_result(self.experiment.job, self.experiment.config)
                if 'email' in self.experiment.job['metadata']:
                    self.mail_sender.send_mail(self.experiment.job['metadata']['email'],
                              self.experiment.job['metadata']['name'],
                              self.experiment.job['timestamp']['datetime'])

            self.experiment.status = Status.DONE
            self.experiment.progress = ProgressStatus.FINISHED


def do_nothing(event_listener, kwargs):
    """do_nothing only exists so that pylint stops complaining."""
    if event_listener or kwargs:
        print(kwargs)