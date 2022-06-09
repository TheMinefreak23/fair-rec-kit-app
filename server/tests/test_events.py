"""
This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from typing import Any
from project.events import Status, ProgressStatus, EventHandler

class TestClassHelper():
    """Class with an status and progress attribute used for testing."""
    status = Any
    progress = Any

class TestClass():
    """Class with an experiment attribute used for testing."""
    experiment = TestClassHelper

Self = TestClass
Self.experiment.status = Status
Self.experiment.progress = ProgressStatus
eventListener = Any

def test_events():
    """Tests the events to see if they correctly change the status and progress attributes."""
    EventHandler.on_parse(Self, eventListener, {})
    assert Self.experiment.progress == ProgressStatus.PARSING

    EventHandler.on_data(Self, eventListener, {})
    assert Self.experiment.progress == ProgressStatus.PROCESSING_DATA

    EventHandler.on_filter(Self, eventListener, {})
    assert Self.experiment.progress == ProgressStatus.FILTERING_DATA

    EventHandler.on_split(Self, eventListener, {})
    assert Self.experiment.progress == ProgressStatus.SPLITTING_DATA

    EventHandler.on_model(Self, eventListener, {})
    assert Self.experiment.progress == ProgressStatus.MODEL

    EventHandler.on_load(Self, eventListener, {})
    assert Self.experiment.progress == ProgressStatus.MODEL_LOAD

    EventHandler.on_train(Self, eventListener, {})
    assert Self.experiment.progress == ProgressStatus.TRAINING

    EventHandler.on_begin_experiment(Self, eventListener, {})
    assert Self.experiment.status == Status.ACTIVE
    assert Self.experiment.progress == ProgressStatus.STARTED
