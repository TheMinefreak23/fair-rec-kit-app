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
from fairreckitlib.core.parsing.parse_event import ON_PARSE
from fairreckitlib.data.pipeline.data_event \
    import ON_BEGIN_DATA_PIPELINE, ON_BEGIN_FILTER_DATASET, \
    ON_BEGIN_SPLIT_DATASET
from fairreckitlib.experiment.experiment_event \
    import ON_BEGIN_EXPERIMENT_THREAD
from fairreckitlib.model.pipeline.model_event \
    import ON_BEGIN_LOAD_TRAIN_SET, ON_BEGIN_MODEL_PIPELINE, \
    ON_BEGIN_TRAIN_MODEL

from project.models.events import Status, ProgressStatus, EventHandler

@dataclass
class TestClassHelper:
    """Class with an status and progress attribute used for testing."""

    status = Any
    progress = Any

@dataclass
class TestClass:
    """Class with an experiment attribute used for testing."""

    experiment = TestClassHelper


Self = TestClass
Self.experiment.status = Status
Self.experiment.progress = ProgressStatus
eventListener = Any


def test_events():
    """Tests the events to see if they correctly change the status and progress attributes."""
    event_handler = EventHandler(Self.experiment, None, None)

    event_handler.handle_event(eventListener, EventArgs(event_id=ON_PARSE))
    assert Self.experiment.progress == ProgressStatus.PARSING

    event_handler.handle_event(eventListener, EventArgs(event_id=ON_BEGIN_DATA_PIPELINE))
    assert Self.experiment.progress == ProgressStatus.PROCESSING_DATA

    event_handler.handle_event(eventListener, EventArgs(event_id=ON_BEGIN_FILTER_DATASET))
    assert Self.experiment.progress == ProgressStatus.FILTERING_DATA

    event_handler.handle_event(eventListener, EventArgs(event_id=ON_BEGIN_SPLIT_DATASET))
    assert Self.experiment.progress == ProgressStatus.SPLITTING_DATA

    event_handler.handle_event(eventListener, EventArgs(event_id=ON_BEGIN_MODEL_PIPELINE))
    assert Self.experiment.progress == ProgressStatus.MODEL

    event_handler.handle_event(eventListener, EventArgs(event_id=ON_BEGIN_LOAD_TRAIN_SET))
    assert Self.experiment.progress == ProgressStatus.MODEL_LOAD

    event_handler.handle_event(eventListener, EventArgs(event_id=ON_BEGIN_TRAIN_MODEL))
    assert Self.experiment.progress == ProgressStatus.TRAINING

    event_handler.handle_event(eventListener, EventArgs(event_id=ON_BEGIN_EXPERIMENT_THREAD))
    assert Self.experiment.status == Status.ACTIVE
    assert Self.experiment.progress == ProgressStatus.STARTED
