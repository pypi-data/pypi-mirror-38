"""Celery tasks: post log to cloudwatch"""
import json  # type: ignore

import celery  # type: ignore
import redis  # type: ignore
from celery import shared_task  # type: ignore
from django.utils import timezone  # type: ignore

import app_settings as app_settings
from cloudwatch import CloudWatchLog

r = redis.StrictRedis()
pipe = r.pipeline()


def store_to_redis(data, name='logbacklog'):
    """
    Stores a python dictionary to the specified redis queue
    :param data: a python dictionary
    :param name: name of the redis queue
    :return: None
    """
    json_data = json.dumps(data)
    pipe.rpush(name, json_data)
    pipe.execute()


def fetch_from_redis(name='logbacklog'):
    """
    Loads data from redis and turns it into a (python) list of dicts
    :param name:
    :return: List of python dictionaries
    """
    pipe.lrange(name, 0, -1)
    redis_data = pipe.execute()
    data = []
    for entry in redis_data[0]:
        data.append(json.loads(entry))
    return data


class LogToCloudWatchBase(celery.Task):
    """Create log object"""
    _cw = None

    @property
    def cw(self):
        """Get cw-log object"""
        if self._cw is None:
            self._cw = CloudWatchLog()
        return self._cw


@shared_task
def log_to_redis(**log_data):
    """Store log in redis"""

    try:
        store_to_redis(log_data)
        log_from_cloudwatch.delay()

    except Exception as e:
        print('Exception', e)
        log_to_redis.retry(
            countdown=2 ** log_to_redis.request.retries, exc=e,
        )


@celery.task(base=LogToCloudWatchBase, max_retries=10, rate_limit=5)
def log_from_cloudwatch(name='logbacklog'):
    """Create log or display error"""

    try:
        # Logs should be send as groups and only after a set interval
        # the interval is demarcated by the 'queue_occupied' value on redis
        if not r.get('queue_occupied'):
            log_data = fetch_from_redis()

            # A post command should not contain empty data, nor
            # should a deletion command be triggered before the logs
            # have been pushed to cloudwatch
            if len(log_data) > 0:
                log_from_cloudwatch.cw.put_logs(log_data)
                pipe.delete(name)

                # Occupy the queue untill the interval has passed.
                pipe.set(
                    'queue_occupied', timezone.now(),
                    ex=app_settings.LOG_INTERVAL,
                )
                pipe.execute()

    except Exception as e:
        print('Exception', e)
        log_from_cloudwatch.retry(
            countdown=2 ** log_from_cloudwatch.request.retries, exc=e,
        )
