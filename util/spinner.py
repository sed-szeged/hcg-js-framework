import sys
import time
import threading
import os

class Spinner:
    busy = False
    delay = 0.1
    text = None

    @staticmethod
    def spinning_cursor():
        while 1:
            for cursor in '|/-\\':
                yield cursor

    def __init__(self, text=None, delay=None):
        self.spinner_generator = self.spinning_cursor()
        self.text = " " + text
        if delay and float(delay):
            self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            if self.text:
                sys.stdout.write(self.text)
                for c in self.text:
                    sys.stdout.write('\b')
            sys.stdout.write('\b')
            sys.stdout.flush()

    def __enter__(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def __exit__(self, exception, value, tb):
        self.busy = False
        time.sleep(self.delay)
        if exception is not None:
            return False