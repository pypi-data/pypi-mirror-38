"""
Tests for module

- Make sure the decorator is working
- Make sure non-decorated models are not being logged
"""
from django.contrib.auth.models import User  # type: ignore
from django.db import models  # type: ignore
from django.test import TestCase  # type: ignore
from django.test.utils import override_settings  # type: ignore

from signals import auditlogger_update_delete  # type: ignore

# build in try/except for python2
try:
    from unittest.mock import patch as patch  # noqa
except ImportError:
    from mock import patch as patch  # type: ignore  # noqa


@auditlogger_update_delete
class LoggedTestModel(models.Model):
    """Test model that is being logged"""
    name = models.CharField(max_length=100, default='LoggedTestModel')


class TestModel(models.Model):
    """Test model that is not being logged"""
    name = models.CharField(max_length=100, default='TestModel')


class TestDecoratorSignals(TestCase):
    """
    Make sure that the signals of the decorated models
    are processed correctly
    """

    def setUp(self):  # type () -> None
        """Setup the testing environment"""
        self.logged_instance = LoggedTestModel()
        self.other_instance = TestModel()

    def test_testmodels_exist_with_correct_values(self):  # type () -> None
        """Make sure all of the classes have the correct ground truth"""
        self.assertEqual(self.other_instance.name, 'TestModel')
        self.assertEqual(self.logged_instance.name, 'LoggedTestModel')

    @override_settings(CELERY_ALWAYS_EAGER=True)
    def test_signals_on_logged_models(self):  # type () -> None
        """Test the 'create' and 'edit' signals"""

        # Mock task, as we dont want to send an actual log
        with patch('auditlogger.tasks.log_from_cloudwatch.delay') as mock_task:

            # Create
            self.logged_instance.save()
            # self.assertTrue(self.signal_was_called)
            self.assertTrue(mock_task.called)

            # Reset signal detector and test edit
            self.signal_was_called = False
            self.logged_instance.name = 'ChangedName'
            self.logged_instance.save()
            # self.assertTrue(self.signal_was_called)
            self.assertTrue(mock_task.called)

            # Reset signal detector and test delete
            self.signal_was_called = False
            self.logged_instance.delete()
            # self.assertTrue(self.signal_was_called)
            self.assertTrue(mock_task.called)

    def test_signals_on_models_that_are_not_logged(self):  # type () -> None
        """
        Test that models that are not being logged don't emmit any signals
        """

        # Mock task, as we dont want to send an actual log
        with patch('auditlogger.tasks.log_from_cloudwatch.delay') as mock_task:

            # Create normal instance, assert signal was not called
            self.other_instance.save()
            self.assertFalse(mock_task.called)


class TestUserSignals(TestCase):
    """
    Test that manipulation of the default User object triggers log actions
    """

    def setUp(self):  # type () -> None
        """Setup testing environment"""
        self.user = User.objects.create_user(
            'TestUser', 'test@example.com', 123,
        )

    def test_altering_user_fields_triggers_signals(self):
        """
        Make sure that changes to objects using the default User model
        trigger log actions
        """
        with patch('auditlogger.tasks.log_from_cloudwatch.delay') as mock_task:  # noqa
                # type () -> None
            self.client.login(username='TestUser', password='123')
            self.assertTrue(mock_task.called)
