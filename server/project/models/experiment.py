"""This file defines different classes required to handle the progress of experiments.

It also handles the experiment itself, which in turn has methods
to run new experiments or validate them.

classes:
    Enum
    ProgressStatus
    QueueItem
    Experiment
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
import enum
import os
from dataclasses import dataclass
import yaml
from fairreckitlib.experiment.experiment_config_parser import ExperimentConfigParser

# Constants
CONFIG_DIR = 'config_files'


class Status(enum.Enum):
    """Experiment status in queue."""
    TODO = 'To Do'
    ACTIVE = 'Active'
    ABORTED = 'Aborted'
    CANCELLED = 'Cancelled'
    DONE = 'Done'
    NA = 'Not Available'


class ProgressStatus(enum.Enum):
    """Experiment progress status."""

    STARTED = 'Started'
    PARSING = 'Parsing'
    EXPERIMENT = 'Started experiment'
    PROCESSING_DATA = 'Processing Data'
    LOADING_DATA = 'Loading Data'
    FILTERING_DATA = 'Filtering Data'
    CONVERTING_DATA = 'Converting Data Ratings'
    SPLITTING_DATA = 'Splitting Data'
    SAVING_DATA = 'Saving Data'
    MODEL = 'Starting approach'
    MODEL_RECONSTRUCTING = 'Reconstructing ratings'
    MODEL_LOAD = 'Loading train set'
    MODEL_TRAINING = 'Training'
    MODEL_TESTING = 'Testing'
    EVALUATING = 'Evaluating'
    EVAL_FILTERING = 'Filtering ratings'
    FINISHED = 'Finished'
    NA = 'Not Available'

@dataclass
class Progress:
    """Dataclass for showing the progress of an experiment."""
    status: ProgressStatus
    progress: int # Progress out of 100
    message: str


def progress_to_dict(progress):
    """Convert progress to dictionary format.

    Args:
        progress: the progress indication

    Returns:
        the converted progress
    """
    return {'status': progress.status.value,
            'number': progress.progress,
            'message': progress.message}

# TODO refactor job and config_dict overlap
@dataclass
class QueueItem:
    """Dataclass for experiment setting items in the queue."""
    job: dict
    config: dict
    status: Status
    progress: Progress
    name: str
    validating: bool = False


class Experiment:
    """For running a recommender system experiment.

    methods:
        __init__
        to_dict
        run_new_experiment
        validate_experiment
    """

    def __init__(self, queue_item, recommender_system):
        """Initialize Experiment class.

        args:
            queue_item(obj): the queue item
            recommender_system(obj): the recommender system (used for retrieving config settings)
        """
        self.queue_item = queue_item
        self.recommender_system = recommender_system

    def to_dict(self):
        """Convert queue item to dictionary format.

        Returns:
            The QueueItem as a dictionary
        """
        self.queue_item.job['status'] = self.queue_item.status.value
        self.queue_item.job['progress'] = progress_to_dict(self.queue_item.progress)
        return self.queue_item.job

    def run_new_experiment(self, events):
        """Run a new experiment (first run).

        Args:
            experiment(QueueItem): the experiment to run

        """
        # Create config files directory if it doesn't exist yet.
        if not os.path.isdir(CONFIG_DIR):
            os.mkdir(CONFIG_DIR)

        # TODO DON'T USE YML?
        # Save configuration to yaml file.
        config_file_path = os.path.join(CONFIG_DIR, self.queue_item.name)

        with open(config_file_path + '.yml', 'w+', encoding='utf-8') as config_file:
            yaml.dump(self.queue_item.config, config_file)

        parser = ExperimentConfigParser(True)
        config = parser.parse_experiment_config_from_yml(config_file_path,
                                                         self.recommender_system.data_registry,
                                                         self.recommender_system.experiment_factory)

        self.recommender_system.run_experiment(config, events=events)

        # Delete temporary YML config
        os.remove(config_file_path + '.yml')


    def validate_experiment(self, events):
        """Validate an experiment by running it multiple times, using the experiment file path.

        Args:
            experiment(QueueItem): the experiment to validate
        """
        self.recommender_system.validate_experiment(result_dir=self.queue_item.job['file_path'],
                                               num_runs=self.queue_item.job['amount'],
                                               events=events)
