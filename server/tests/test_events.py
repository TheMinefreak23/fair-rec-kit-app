"""This module tests the event_handler events to see if the progress and status change.

TestClassHelper: class with an status and progress attribute used for testing.
TestClass: class with an experiment attribute used for testing.
test_events(): tests the events to see if they correctly change the status and progress attributes.

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from dataclasses import dataclass
from typing import Any

from fairreckitlib.core.events.event_args import EventArgs
from fairreckitlib.data.pipeline.data_event \
    import ON_BEGIN_DATA_PIPELINE, ON_BEGIN_FILTER_DATASET, \
    ON_BEGIN_SPLIT_DATASET
from fairreckitlib.experiment.experiment_event \
    import ON_BEGIN_EXPERIMENT_THREAD, ExperimentThreadEventArgs, ON_END_EXPERIMENT_THREAD
from fairreckitlib.model.pipeline.model_event \
    import ON_BEGIN_LOAD_TRAIN_SET, ON_BEGIN_MODEL_PIPELINE, \
    ON_BEGIN_TRAIN_MODEL

from project.models.events import Status, Progress, ProgressStatus, EventHandler


@dataclass
class TestClassHelper:
    """Class with an status and progress attribute used for testing."""

    status = ProgressStatus
    progress = Progress
    validating = True


@dataclass
class TestClass:
    """Class with an experiment attribute used for testing."""

    experiment = TestClassHelper


Self = TestClass
Self.experiment.status = Status
Self.experiment.progress = Progress
eventListener = Any


def test_events():
    """Tests the events to see if they correctly change the status and progress attributes."""
    event_handler = EventHandler(Self.experiment, None, None)
    event_handler.max_progress = 100

    event_handler.handle_event(eventListener, EventArgs(event_id=ON_BEGIN_DATA_PIPELINE))
    assert Self.experiment.progress.status == ProgressStatus.PROCESSING_DATA

    event_handler.handle_event(eventListener, EventArgs(event_id=ON_BEGIN_FILTER_DATASET))
    assert Self.experiment.progress.status == ProgressStatus.FILTERING_DATA

    event_handler.handle_event(eventListener, EventArgs(event_id=ON_BEGIN_SPLIT_DATASET))
    assert Self.experiment.progress.status == ProgressStatus.SPLITTING_DATA

    event_handler.handle_event(eventListener, EventArgs(event_id=ON_BEGIN_MODEL_PIPELINE))
    assert Self.experiment.progress.status == ProgressStatus.MODEL

    event_handler.handle_event(eventListener, EventArgs(event_id=ON_BEGIN_LOAD_TRAIN_SET))
    assert Self.experiment.progress.status == ProgressStatus.MODEL_LOAD

    event_handler.handle_event(eventListener, EventArgs(event_id=ON_BEGIN_TRAIN_MODEL))
    assert Self.experiment.progress.status == ProgressStatus.MODEL_TRAINING

    event_handler.handle_event(eventListener,
                               ExperimentThreadEventArgs(event_id=ON_BEGIN_EXPERIMENT_THREAD,
                                                         num_runs=0,
                                                         experiment_name='foo'),
                               elapsed_time=0)
    assert Self.experiment.status == Status.ACTIVE
    assert Self.experiment.progress.status == ProgressStatus.STARTED

    event_handler.handle_event(eventListener,
                               ExperimentThreadEventArgs(event_id=ON_END_EXPERIMENT_THREAD,
                                                         num_runs=0,
                                                         experiment_name='foo'),
                               elapsed_time=0)
    assert Self.experiment.status == Status.DONE
    assert Self.experiment.progress.status == ProgressStatus.FINISHED
    assert Self.experiment.progress.message == 'Finished 0 experiment(s) with name foo in 0.0000s'
