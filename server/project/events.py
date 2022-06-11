"""
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
from .mail import send_mail
from .result_storage import save_result
from .experiment import Status, ProgressStatus


class EventHandler():
    """Handles the events"""
    def __init__(self, experiment, end_experiment):
        self.experiment = experiment
        self.end_experiment = end_experiment
        self.events = {
            #ON_BEGIN_EXPERIMENT_PIPELINE: lambda x, **kwargs: print('uwu'),
            #ON_END_EXPERIMENT_PIPELINE: self.on_end_experiment,
            ON_BEGIN_EXPERIMENT_THREAD: self.on_begin_experiment,
            ON_END_EXPERIMENT_THREAD: self.on_end_experiment_thread,
            ON_PARSE: self.on_parse,  # NOTE TODO doesn't work in backend
            ON_BEGIN_DATA_PIPELINE: self.on_data,
            ON_BEGIN_FILTER_DATASET: self.on_filter,
            ON_BEGIN_SPLIT_DATASET: self.on_split,
            ON_BEGIN_MODEL_PIPELINE: self.on_model,
            ON_BEGIN_LOAD_TRAIN_SET: self.on_load,
            ON_BEGIN_TRAIN_MODEL: self.on_train,
        }

    def on_parse(self, event_listener, event_args, **kwargs):
        """Change progress status to parsing."""
        do_nothing(event_listener, event_args, kwargs)
        self.experiment.progress = ProgressStatus.PARSING

    def on_data(self, event_listener, event_args, **kwargs):
        """Change progress status to processing data."""
        do_nothing(event_listener, event_args, kwargs)
        self.experiment.progress = ProgressStatus.PROCESSING_DATA

    def on_filter(self, event_listener, event_args, **kwargs):
        """Change progress status to filtering data."""
        do_nothing(event_listener, event_args, kwargs)
        self.experiment.progress = ProgressStatus.FILTERING_DATA

    def on_split(self, event_listener, event_args, **kwargs):
        """Change progress status to splitting data."""
        do_nothing(event_listener, event_args, kwargs)
        self.experiment.progress = ProgressStatus.SPLITTING_DATA

    def on_model(self, event_listener, event_args, **kwargs):
        """Change progress status to model."""
        do_nothing(event_listener, event_args, kwargs)
        self.experiment.progress = ProgressStatus.MODEL

    def on_load(self, event_listener, event_args, **kwargs):
        """Change progress status to model load."""
        do_nothing(event_listener, event_args, kwargs)
        self.experiment.progress = ProgressStatus.MODEL_LOAD

    def on_train(self, event_listener, event_args, **kwargs):
        """Change progress status to training."""
        do_nothing(event_listener, event_args, kwargs)
        self.experiment.progress = ProgressStatus.TRAINING

    def on_begin_experiment(self, event_listener, event_args, **kwargs):
        """Change progress status to started
        and update the experiment status to active."""
        do_nothing(event_listener, event_args, kwargs)
        self.experiment.status = Status.ACTIVE
        self.experiment.progress = ProgressStatus.STARTED

    def on_end_experiment_thread(self, event_listener, event_args, **kwargs):
        """Change progress status to finished
        and experiment status to done.
        Also sends an email if possible."""
        do_nothing(event_listener, event_args, kwargs)
        if self.experiment.status is not Status.ABORTED:
            if not self.experiment.validating:
                # TODO Update experiment data: Save elapsed time
                #self.experiment.job['metadata']['duration'] = kwargs['elapsed_time']
                save_result(self.experiment.job, self.experiment.config)
                if 'email' in self.experiment.job['metadata']:
                    send_mail(self.experiment.job['metadata']['email'],
                          self.experiment.job['metadata']['name'],
                          self.experiment.job['timestamp']['datetime'])
            #else: self.experiment.job['runs'] = kwargs['num_runs']

            self.experiment.status = Status.DONE
            self.experiment.progress = ProgressStatus.FINISHED
        self.end_experiment()

def do_nothing(event_listener, event_args, kwargs):
    """This function only exists so that pylint stops complaining."""
    event_listener
    event_args
    kwargs
