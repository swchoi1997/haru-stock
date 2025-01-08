import time
from queue import Queue

from MessageBridge.MessageBridge import MessageConsumer


class InnerQueueConsumer(MessageConsumer):
    def __init__(self, process_message_callback, inner_queue: Queue):
        self.process_message_callback = process_message_callback
        self.inner_queue = inner_queue

    def consume(self, is_running):
        while is_running:
            try:
                message = self.inner_queue.get()

                self.process_message_callback(message)
            finally:
                time.sleep(0.1)
