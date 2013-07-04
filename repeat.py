import time

__author__ = 'Christopher'


def every(task, seconds=60):
    while True:
        time.sleep(seconds)
        task()
