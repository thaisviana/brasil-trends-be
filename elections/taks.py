from celery.schedules import crontab
from celery.task.base import periodic_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@periodic_task(run_every=crontab(minute='*/2'), name='test', ignore_result=True)
def test():
    print("=== FINISHED ===")
