"""This file handles events from the fairreckitlib library, e.g. an experiment finish.

classes:
    EventHandler

methods:
    do_nothing

This program has been developed by students from the bachelor Computer Science at
Utrecht University within the Software Project course.
© Copyright Utrecht University (Department of Information and Computing Sciences)
"""
from fairreckitlib.evaluation.pipeline.evaluation_event import \
    ON_BEGIN_EVAL_PIPELINE, ON_BEGIN_FILTER_RECS
from fairreckitlib.experiment.experiment_event import \
    ON_END_EXPERIMENT_THREAD, ON_BEGIN_EXPERIMENT_THREAD, \
    ON_BEGIN_EXPERIMENT_PIPELINE
from fairreckitlib.model.pipeline.model_event import \
    ON_BEGIN_MODEL_PIPELINE, ON_BEGIN_TRAIN_MODEL,\
    ON_BEGIN_LOAD_TRAIN_SET, ON_BEGIN_RECONSTRUCT_RATINGS,\
    ON_BEGIN_TEST_MODEL
from fairreckitlib.data.pipeline.data_event import \
    ON_BEGIN_DATA_PIPELINE, ON_BEGIN_FILTER_DATASET, \
    ON_BEGIN_SPLIT_DATASET, \
    ON_BEGIN_CONVERT_RATINGS, ON_BEGIN_SAVE_SETS
from .experiment import Status, ProgressStatus, Progress, current_dt

PROGRESS_DICT = {
    ON_BEGIN_EXPERIMENT_PIPELINE: ProgressStatus.EXPERIMENT,
    ON_BEGIN_DATA_PIPELINE: ProgressStatus.PROCESSING_DATA,
    # ON_BEGIN_LOAD_DATASET: ProgressStatus.LOADING_DATA,
    ON_BEGIN_FILTER_DATASET: ProgressStatus.FILTERING_DATA,
    ON_BEGIN_CONVERT_RATINGS: ProgressStatus.CONVERTING_DATA,
    ON_BEGIN_SPLIT_DATASET: ProgressStatus.SPLITTING_DATA,
    ON_BEGIN_SAVE_SETS: ProgressStatus.SAVING_DATA,
    ON_BEGIN_MODEL_PIPELINE: ProgressStatus.MODEL,
    ON_BEGIN_RECONSTRUCT_RATINGS: ProgressStatus.MODEL_RECONSTRUCTING,
    ON_BEGIN_LOAD_TRAIN_SET: ProgressStatus.MODEL_LOAD,
    ON_BEGIN_TRAIN_MODEL: ProgressStatus.MODEL_TRAINING,
    ON_BEGIN_TEST_MODEL: ProgressStatus.MODEL_TESTING,
    ON_BEGIN_EVAL_PIPELINE: ProgressStatus.EVALUATING,
    ON_BEGIN_FILTER_RECS: ProgressStatus.EVAL_FILTERING
}

STATUS_ORDER = [
    ProgressStatus.EXPERIMENT,
    ProgressStatus.PROCESSING_DATA,
    ProgressStatus.LOADING_DATA,
    ProgressStatus.FILTERING_DATA,
    ProgressStatus.CONVERTING_DATA,
    ProgressStatus.SPLITTING_DATA,
    ProgressStatus.SAVING_DATA,
    ProgressStatus.MODEL,
    ProgressStatus.MODEL_LOAD,
    ProgressStatus.MODEL_TRAINING,
    ProgressStatus.MODEL_TESTING,
    ProgressStatus.MODEL_RECONSTRUCTING,
    ProgressStatus.EVALUATING,
    ProgressStatus.EVAL_FILTERING
]


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
        self.current_index = 0  # Index of current (sub-)experiment in thread
        self.max_progress = 0
        event_ids = [
            ON_BEGIN_EXPERIMENT_THREAD,
            ON_BEGIN_EXPERIMENT_PIPELINE,
            ON_BEGIN_DATA_PIPELINE,
            # ON_BEGIN_LOAD_DATASET,
            ON_BEGIN_FILTER_DATASET,
            ON_BEGIN_CONVERT_RATINGS,
            ON_BEGIN_SPLIT_DATASET,
            ON_BEGIN_SAVE_SETS,
            ON_BEGIN_MODEL_PIPELINE,
            ON_BEGIN_RECONSTRUCT_RATINGS,
            ON_BEGIN_LOAD_TRAIN_SET,
            ON_BEGIN_TRAIN_MODEL,
            ON_BEGIN_TEST_MODEL,
            ON_BEGIN_EVAL_PIPELINE,
            ON_BEGIN_FILTER_RECS,
            # ON_END_EXPERIMENT_PIPELINE,
            ON_END_EXPERIMENT_THREAD,
        ]
        self.events = {event_id: self.handle_event for event_id in event_ids}

    def handle_event(self, event_listener, event_args, **kwargs):
        """Handle the event based on its ID.

        args:
            event_listener(obj): the event_listener to be used
            event_args(dict): the event arguments
        """
        if not event_listener: # TODO this is only done so pylint stops yappin'
            print('No event listener')

        if event_args.event_id == ON_BEGIN_EXPERIMENT_THREAD:
            self.on_begin_experiment_thread(event_args)
        elif event_args.event_id == ON_END_EXPERIMENT_THREAD:
            self.on_end_experiment_thread(event_args, kwargs)
        else:
            # Change progress status.
            progress_status = PROGRESS_DICT[event_args.event_id]
            progress_number = int(self.current_index *
                                  (STATUS_ORDER.index(progress_status) + 1) /
                                  self.max_progress * 100)
            #print('CURRENT INDEX', self.current_index,
            #      'MAX PROGRESS', self.max_progress,
            #      'RELATIVE PROGRESS', (self.current_index *
            #                      (STATUS_ORDER.index(progress_status) + 1) /
            #                      self.max_progress),
            #      'PROGRESS NUMBER', progress_number)
            self.experiment.progress = Progress(
                status=progress_status,
                progress=progress_number,
                message=progress_status.value
            )
            if event_args.event_id == ON_BEGIN_EXPERIMENT_PIPELINE:
                self.current_index += 1
                # print('ON BEGIN EXP CURRENT INDEX', self.current_index)

    def on_begin_experiment_thread(self, args):
        """Change progress status to started and update the experiment status to active."""
        self.experiment.status = Status.ACTIVE
        self.experiment.progress = Progress(
            status=ProgressStatus.STARTED,
            progress=0,
            message='')

        # Set maximal progress number based on runs
        self.max_progress = args.num_runs * len(STATUS_ORDER)

        # Add experiment execution data to settings
        self.experiment.job.setdefault('experiments', []).append({'started': current_dt()})


    def on_end_experiment_thread(self, args, kwargs):
        """Change progress status to finished and experiment status to "done".

        Also sends an email if possible.
        """
        if self.experiment.status is not Status.ABORTED:
            # Execution data
            elapsed_time = kwargs['elapsed_time']
            last_exp = self.experiment.job['experiments'][-1]
            last_exp['ended'] = current_dt()
            last_exp['elapsed_time'] = elapsed_time

            if not self.experiment.validating:
                # Save result and send mail
                self.experiment.job['experiments'][-1] = last_exp
                self.result_storage.save_result(self.experiment.job,
                                                self.experiment.config)
                if 'email' in self.experiment.job['metadata']:
                    self.mail_sender.send_mail(self.experiment.job)
            else:
                # Update entry with execution data
                last_exp['runs'] = self.experiment.job['amount']
                self.result_storage.update_result(self.experiment.job['overview_index'],
                                                  last_exp)

            # Update progress and status
            self.experiment.progress = Progress(
                status=ProgressStatus.FINISHED,
                progress=100,
                message=f'Finished {args.num_runs} experiment(s) '
                        f'with name {args.experiment_name} in '
                        f'{elapsed_time:1.4f}s'
            )
            self.experiment.status = Status.DONE
