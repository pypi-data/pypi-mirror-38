"""Classes to publish logs to aws"""
import json
import time

import boto3  # type: ignore
from botocore.config import Config  # type: ignore
from botocore.exceptions import ClientError  # type: ignore

import app_settings as app_settings  # type: ignore

# Limit the number of retries to 3, to stay under the rate limit
CONFIG = Config(
    retries=dict(
        max_attempts=3,
    ),
)


class AuditLoggerException(Exception):
    """Custom exception for the application"""
    pass


class CloudWatchLog:
    """Facilitates the connection to AWS"""
    next_sequence_token = None

    def __init__(self):  # type () -> None
        self.validate_settings()

        self.client = boto3.client(
            'logs',
            region_name=app_settings.AUDIT_LOGGER_REGION,
            aws_access_key_id=app_settings.AUDIT_LOGGER_KEY_ID,
            aws_secret_access_key=app_settings.AUDIT_LOGGER_SECRET_ACCESS_KEY,
            config=CONFIG,
        )

    @staticmethod
    def validate_settings():  # type () -> None
        """Make sure that the correct settings exist"""

        required_settings = [
            'AUDIT_LOGGER_REGION',
            'AUDIT_LOGGER_KEY_ID',
            'AUDIT_LOGGER_SECRET_ACCESS_KEY',
            'AUDIT_LOGGER_GROUP_NAME',
            'AUDIT_LOGGER_STREAM_NAME',
        ]

        for setting_name in required_settings:
            if not getattr(app_settings, setting_name):
                raise AuditLoggerException(
                    'Setting: {} not defined'.format(setting_name),
                )

    def create_log_group(self):  # type () -> None
        """Create (or skip) a loggroup"""
        # Try creating the log group
        try:
            self.client.create_log_group(
                logGroupName=app_settings.AUDIT_LOGGER_GROUP_NAME,
            )
        except ClientError:
            # The group probably already exists. We can just continue on
            # with the rest.
            pass

    def create_log_stream(self):  # type () -> None
        """Create (or skip) a logstream"""
        self.create_log_group()

        # Try creating the log stream
        try:
            self.client.create_log_stream(
                logGroupName=app_settings.AUDIT_LOGGER_GROUP_NAME,
                logStreamName=app_settings.AUDIT_LOGGER_STREAM_NAME,
            )
        except ClientError:
            # The stream probably already exists. We can just continue on
            # with the rest.
            pass

    def put_logs(self, log_data):  # type () -> None
        """Create new log objects and pass them to aws"""
        self.create_log_stream()

        log_events = []

        for log in log_data:
            entry = {
                'timestamp': int(time.time()) * 1000,
                'message': json.dumps(log),

            }
            log_events.append(entry)

        try:
            kwargs = dict(
                logGroupName=app_settings.AUDIT_LOGGER_GROUP_NAME,
                logStreamName=app_settings.AUDIT_LOGGER_STREAM_NAME,
                logEvents=log_events,
            )

            if self.next_sequence_token:
                kwargs['sequenceToken'] = self.next_sequence_token

            response = self.client.put_log_events(**kwargs)
            self.next_sequence_token = response.get('nextSequenceToken')

        except ClientError as e:
            if e.response.get('Error', {}).get('Code') in (
                    'DataAlreadyAcceptedException',
                    'InvalidSequenceTokenException'):
                self.next_sequence_token = \
                    e.response['Error']['Message'].rsplit(' ', 1)[-1]
                self.put_logs(log_data)
                return
            else:
                raise

        return
