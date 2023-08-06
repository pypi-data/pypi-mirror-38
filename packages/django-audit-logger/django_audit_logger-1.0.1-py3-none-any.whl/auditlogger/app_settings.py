"""App specific settings"""
from django.conf import settings  # type: ignore

AUDIT_LOGGER_REGION = getattr(settings, 'AUDIT_LOG_REGION', 'eu-west-1')
AUDIT_LOGGER_KEY_ID = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
AUDIT_LOGGER_SECRET_ACCESS_KEY = getattr(
    settings, 'AWS_SECRET_ACCESS_KEY', None,
)
AUDIT_LOGGER_GROUP_NAME = getattr(settings, 'AUDIT_LOG_GROUP_NAME', None)
AUDIT_LOGGER_STREAM_NAME = getattr(settings, 'AUDIT_LOG_STREAM_NAME', None)
AUDIT_LOGGER_EXCLUDE = getattr(settings, 'AUDIT_LOG_EXCLUDE', [])
# Interval value represents minutes
LOG_INTERVAL = getattr(settings, 'LOG_INTERVAL', 5)
