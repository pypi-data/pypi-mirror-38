# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import time

from azureml._logging import ChainedIdentity

from .async_task import AsyncTask
from .worker_pool import WorkerPool

DEFAULT_PRIORITY = 1


class TaskQueue(ChainedIdentity):
    """
    A class for managing async tasks. This class is not threadsafe.
    """

    def __init__(self, worker_pool=None, error_handler=None, **kwargs):
        """
        :param worker_pool: Thread pool for executing tasks
        :type worker_pool: concurrent.futures.ThreadPoolExecutor
        :param error_handler: Extension point for processing error queue items
        :type error_handler: function(error, logging.Logger)
        """
        super(TaskQueue, self).__init__(**kwargs)
        self._tasks = []
        self._results = []
        # For right now, don't need queue for errors, but it's
        # probable that we'll want the error handler looping on queue thread
        self._errors = []
        self._err_handler = error_handler
        self._worker_pool = worker_pool if worker_pool is not None else WorkerPool(_parent_logger=self._logger)
        self._task_number = 0

    def __enter__(self):
        self._logger.debug("[Start]")
        return self

    def __exit__(self, *args):
        self._logger.debug("[Stop]")
        self.flush(self.identity)

    def add(self, func, *args, **kwargs):
        """
        :param func: Function to be executed asynchronously
        :type func: builtin.function
        :param task_priority: Priority for the task, higher items have higher priority
        :type task_priority: int or None
        """
        task_priority = kwargs.get("task_priority")
        future = self._worker_pool.submit(func, *args, **kwargs)
        ident = "{}_{}".format(len(self._tasks), func.__name__)
        task = AsyncTask(future, _ident=ident, _parent_logger=self._logger)
        self.add_task(task, task_priority=task_priority)
        return task

    def add_task(self, async_task, task_priority=None):
        """
        :param async_task: asynchronous task to be added to the queue and possibly processed
        :type async_task: azureml._async.AsyncTask
        :param task_priority: Priority for the task, higher items have higher priority
        :type task_priority: int or None
        """
        '''Blocking, no timeout add task to queue'''
        if not isinstance(async_task, AsyncTask):
            raise ValueError("Can only add AsyncTask, got {0}".format(type(async_task)))

        if task_priority is None:
            task_priority = DEFAULT_PRIORITY
        entry = (task_priority, async_task)
        self._logger.debug("Adding task {0} to queue with task priority {1}".format(async_task.ident,
                                                                                    task_priority))
        self._tasks.append(entry)
        self._logger.debug("Queue size is approx. {}".format(len(self._tasks)))

    def flush(self, source):
        with self._log_context("WaitFlushSource:{}".format(source)) as log_context:
            start_time = time.time()
            log_context.debug("Waiting on tasks: {}.".format(self._tasks))
            tasks_to_wait = self._tasks
            self._tasks = []
            not_done = True
            message = ""
            while not_done:
                tasks_left = [(priority, task) for priority, task in tasks_to_wait if not task.done()]
                not_done = len(tasks_left) != 0

                for priority, task in tasks_left:
                    message += "Waiting on task: {}. With priority {}.\n".format(task.ident, priority)
                message += "{} tasks left. Current duration of flush {} seconds.\n".format(
                    len(tasks_left), time.time() - start_time)

                time.sleep(.1)

            log_context.debug(message)

            self._results.extend((task.wait() for _, task in tasks_to_wait))

    @property
    def results(self):
        for result in self._results:
            yield result

    def errors(self):
        for error in self._errors:
            yield error
