# myapp/tasks.py
from datetime import timedelta
from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger

from fs import Repository

logger = get_task_logger(__name__)

@periodic_task(run_every=timedelta(seconds=30))
def scan():
    logger.info("Checking directory...")
    repository = Repository('/Users/Willi/pdf')

    while True:
        document = repository.next()

        if document is None:
            break

        logger.info("Found " + document)

    logger.info("done")
