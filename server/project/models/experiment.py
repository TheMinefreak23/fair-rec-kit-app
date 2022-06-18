"""
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

# TODO send enums to client?
# def enum_to_dict(enum):
#     return {i.name: i.value for i in enum}

# @compute_bp.route('/statuses', methods=['GET'])
# def get_statuses():
#     return


class Status(enum.Enum):
    """Experiment status in queue"""
    TODO = 'To Do'
    ACTIVE = 'Active'
    ABORTED = 'Aborted'
    CANCELLED = 'Cancelled'
    DONE = 'Done'
    NA = 'Not Available'


class ProgressStatus(enum.Enum):
    """Experiment progress status"""
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


# TODO refactor job and config_dict overlap
@dataclass
class QueueItem:
    """Dataclass for experiment setting items in the queue"""
    job: dict
    config: dict
    status: Status
    progress: ProgressStatus
    name: str
    validating: bool = False


class Experiment:
    """For running a recommender system experiment"""
    def __init__(self, queue_item, recommender_system):
        self.queue_item = queue_item
        self.recommender_system = recommender_system

        """
        # TODO refactor job and config_dict overlap
        self.job =
        self.config =
        self.status = Status.TODO
        self.progress = ProgressStatus.NA
        self.name =
        self.validating =
        """

    def to_dict(self):
        """Convert queue item to dictionary format

        Returns:
            The QueueItem as a dictionary
        """
        # TODO refactor
        self.queue_item.job['status'] = self.queue_item.status.value
        self.queue_item.job['progress'] = self.queue_item.progress.value
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
