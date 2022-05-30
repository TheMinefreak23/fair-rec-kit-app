"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import enum

from fairreckitlib.experiment.experiment_event import ON_END_EXPERIMENT_PIPELINE, ON_END_EXPERIMENT_THREAD, \
    ON_BEGIN_EXPERIMENT_PIPELINE, ON_BEGIN_EXPERIMENT_THREAD
from fairreckitlib.model.pipeline.model_event import ON_BEGIN_MODEL_PIPELINE, ON_BEGIN_TRAIN_MODEL, \
    ON_BEGIN_LOAD_TRAIN_SET
from fairreckitlib.data.pipeline.data_event import ON_BEGIN_DATA_PIPELINE, \
    ON_END_DATA_PIPELINE, ON_BEGIN_FILTER_DATASET, ON_BEGIN_SPLIT_DATASET
from fairreckitlib.core.parsing.parse_event import ON_PARSE
from .mail import send_mail


# Experiment status in queue
class Status(enum.Enum):
    TODO = 'To Do'
    ACTIVE = 'Active'
    ABORTED = 'Aborted'
    CANCELLED = 'Cancelled'
    DONE = 'Done'
    NA = 'Not Available'


""" TODO send enums to client?
def enum_to_dict(enum):
    return {i.name: i.value for i in enum}

@compute_bp.route('/statuses', methods=['GET'])
def get_statuses():
    return 
    """


# Experiment progress status
class ProgressStatus(enum.Enum):
    STARTED = 'Started'
    PARSING = 'Parsing'
    PROCESSING_DATA = 'Processing Data'
    FILTERING_DATA = 'Filtering Data'
    SPLITTING_DATA = 'Splitting Data'
    MODEL = 'Starting approach'
    MODEL_LOAD = 'Loading train set'
    TRAINING = 'Training'
    EVALUATING = 'Evaluating'
    FINISHED = 'Finished'
    NA = 'Not Available'


class EventHandler():
    def __init__(self, experiment, end_experiment):
        self.experiment = experiment
        self.end_experiment = end_experiment
        self.events = {
            ON_BEGIN_EXPERIMENT_PIPELINE: lambda x, **kwargs: print('uwu'),
            ON_END_EXPERIMENT_PIPELINE: lambda x, **kwargs: print('owo'),
            ON_BEGIN_EXPERIMENT_THREAD: self.on_begin_experiment,
            ON_END_EXPERIMENT_THREAD: self.on_end_experiment,
            ON_PARSE: self.on_parse,  # NOTE TODO doesn't work in backend
            ON_BEGIN_DATA_PIPELINE: self.on_data,
            ON_BEGIN_FILTER_DATASET: self.on_filter,
            ON_BEGIN_SPLIT_DATASET: self.on_split,
            ON_BEGIN_MODEL_PIPELINE: self.on_model,
            ON_BEGIN_LOAD_TRAIN_SET: self.on_load,
            ON_BEGIN_TRAIN_MODEL: self.on_train,
        }

    def on_parse(self, event_listener, **kwargs):
        # print('epic')
        self.experiment.progress = ProgressStatus.PARSING

    def on_data(self, event_listener, **kwargs):
        # print('super')
        self.experiment.progress = ProgressStatus.PROCESSING_DATA

    def on_filter(self, event_listener, **kwargs):
        # print('dangan')
        self.experiment.progress = ProgressStatus.FILTERING_DATA

    def on_split(self, event_listener, **kwargs):
        # print('ronpa')
        self.experiment.progress = ProgressStatus.SPLITTING_DATA

    def on_model(self, event_listener, **kwargs):
        # print('2')
        self.experiment.progress = ProgressStatus.MODEL

    def on_load(self, event_listener, **kwargs):
        # print('2')
        self.experiment.progress = ProgressStatus.MODEL_LOAD

    def on_train(self, event_listener, **kwargs):
        # print('2')
        self.experiment.progress = ProgressStatus.TRAINING

    def on_begin_experiment(self, event_listener, **kwargs):
        # Update experiment status
        self.experiment.status = Status.ACTIVE
        self.experiment.progress = ProgressStatus.STARTED

    def on_end_experiment(self, event_listener, **kwargs):
        # TODO get real recs&eval result
        # print('saving job', current_experiment.job)
        # print('config', current_experiment.config)

        # Update status
        if self.experiment.status is not Status.ABORTED:
            self.experiment.status = Status.DONE
            self.experiment.progress = ProgressStatus.FINISHED
            send_mail(self.experiment.job['metadata']['email'],
                  self.experiment.job['metadata']['name'],
                  self.experiment.job['timestamp']['datetime'])

        self.end_experiment()
