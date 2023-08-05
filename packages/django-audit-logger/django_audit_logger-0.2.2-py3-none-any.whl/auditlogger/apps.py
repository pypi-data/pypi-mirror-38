"""Signals are loaded"""
from django.apps import AppConfig


class AuditLoggerConfig(AppConfig):
    """Set name and load signals"""
    name = 'auditlogger'

    def ready(self):
        """Load signals"""
        from auditlogger import signals  # noqa
