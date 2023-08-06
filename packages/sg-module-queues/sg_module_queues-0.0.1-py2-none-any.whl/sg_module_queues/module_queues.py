import copy
import os
import time

from queue import Queue


class ModuleQueues(object):

    def __init__(self, input_queue_key, processing_queue_key, output_queue_key):

        REDIS_URL = os.environ.get('REDIS_URL')

        if REDIS_URL is None:
            raise ValueError("No REDIS_URL in environment")

        # Initialise all queues
        try:
            self.input_queue = Queue(REDIS_URL, input_queue_key)
            self.processing_queue = Queue(REDIS_URL, processing_queue_key)
            self.output_queue = Queue(REDIS_URL, output_queue_key)
        except:
            # Redis initialisation failed or queue couldn't be created
            raise


    def process_task(self, callback):

        task = self.input_queue.get()

        # Keep a copy of unaltered data to remove the correct item from the processing queue upon callback completion
        original_task = copy.deepcopy(task)
        self.processing_queue.put(original_task, time.time())

        try:
            updated_task = callback(task)  # Callback should throw descriptive exceptions
            self.processing_queue.remove(original_task)
            self.output_queue.put(updated_task, time.time())
        except:
            # If something went wrong in the callback
            raise
