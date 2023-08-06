import logging
import signal
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from enum import Enum
from functools import wraps
from queue import Queue
from threading import Thread

logger = logging.getLogger(__name__)
original_on_sigint = signal.getsignal(signal.SIGINT)
pools = []

def on_sigint(sig, frame):
    for pool in pools:
        pool.shutdown()
    return original_on_sigint(sig, frame)

signal.signal(signal.SIGINT, on_sigint)


def threaded(fn):
    wraps(fn)
    def wrapped(*args, **kwargs):
        t = Thread(target=fn, args=args, kwargs=kwargs)
        t.setDaemon(True)
        t.start()
        return t
    return wrapped


def shielded(fn):
    wraps(fn)
    def wrapped(*args, **kwargs):
        try:
            fn(*args, **kwargs)
        except Exception as e:
            fields = {
                'fn': fn.__name__,
                'args': args,
                'kwargs': kwargs,
            }
            logger.error('Worker processment failed', extra=fields)
    return wrapped


class WorkerPoolException(Exception):
    pass


class WorkerPoolStatus(Enum):
    OPEN = 1
    HALF_OPEN = 2
    CLOSED = 3


class WorkerPool:
    """
    Base context manager that exposes the interface for submitting tasks to be
    consumed by workers.

    This class should not be instantiated directly. IOWorkerPool or
    CPUWorkerPool should be used instead.
    """
    def __init__(self, PoolExecutor, max_workers=None, max_queue_size=0):
        """
        Initializes the worker pool.

        :param PoolExecutor: The type of pool executor. Should be either
        ThreadPoolExecutor or ProcessPoolExecutor.

        :param max_workers: Spawns a pool of at most `max_workers`. If not
        specified, it will default to the what the provided PoolExecutor uses
        as default.

        :param max_queue_size: integer that sets the upperbound limit on the
        number of items that can be placed in the queue. Insertion will block
        once this size has been reached, until queue items are consumed. If
        `max_queue_size` is less than or equal to zero, the queue size is
        infinite.
        """
        pools.append(self)
        self.executor = PoolExecutor(max_workers=max_workers)
        self.queue = Queue(maxsize=max_queue_size)
        self.status = WorkerPoolStatus.OPEN
        self.start()

    def __enter__(self):
        self.executor.__enter__()
        return self

    def __exit__(self, type, value, traceback):
        self.shutdown()
        self.executor.__exit__(type, value, traceback)

    def shutdown(self):
        """
        Shuts down the current queue.
        """
        if self.status == WorkerPoolStatus.CLOSED: return
        self.status = WorkerPoolStatus.HALF_OPEN
        self.queue.join()
        self.status = WorkerPoolStatus.CLOSED

    def submit(self, fn, *args, **kwargs):
        """
        Submits a callable that will be invoked like `fn(*args, **kwargs)`, by
        one of the workers.
        """
        if self.status == WorkerPoolStatus.HALF_OPEN:
            return
        if self.status == WorkerPoolStatus.CLOSED:
            error = "Won't process new message"
            raise WorkerPoolException(error)
        else:
            message = (fn, args, kwargs)
            self.queue.put(message)

    @threaded
    def start(self):
        """
        Starts consumption
        """
        while self.status != WorkerPoolStatus.CLOSED:
            message = self.queue.get()
            fn, args, kwargs = message
            self.executor.submit(shielded(fn), *args, **kwargs)
            self.queue.task_done()


class IOWorkerPool(WorkerPool):
    """
    Context manager that exposes the interface for submitting tasks to be
    consumed by workers that will be performing IO-bound operations.
    """
    def __init__(self, max_workers=None, max_queue_size=0):
        """
        Initializes the worker pool.

        :param max_workers: Spawns a pool of at most `max_workers`. If not
        specified, it will default to the numberr of processors on the
        machine, multiplied by 5.

        :param max_queue_size: integer that sets the upperbound limit on the
        number of items that can be placed in the queue. Insertion will block
        once this size has been reached, until queue items are consumed. If
        `max_queue_size` is less than or equal to zero, the queue size is
        infinite.
        """
        super().__init__(ThreadPoolExecutor, max_workers, max_queue_size)


class CPUWorkerPool(WorkerPool):
    """
    Context manager that exposes the interface for submitting tasks to be
    consumed by workers that will be performing CPU-bound operations.
    """
    def __init__(self, max_workers=None, max_queue_size=0):
        """
        Initializes the worker pool.

        :param max_workers: Spawns a pool of at most `max_workers`. If not
        specified, it will default to the numberr of processors on the
        machine.

        :param max_queue_size: integer that sets the upperbound limit on the
        number of items that can be placed in the queue. Insertion will block
        once this size has been reached, until queue items are consumed. If
        `max_queue_size` is less than or equal to zero, the queue size is
        infinite.
        """
        super().__init__(ProcessPoolExecutor, max_workers, max_queue_size)
