import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
from unittest.mock import patch
from src.notifier.runner import notify

class TestNotify(unittest.TestCase):
    @patch('plyer.notification.notify')
    def test_notify_calls_plyer_movement(self, mock_notify):
        title = "Test Title"
        message = "Test Message"
        notify(title, message, "movement")
        mock_notify.assert_called_once_with(
            title=title,
            message=message,
            app_name="Crypto Notifier",
            timeout=5
        )

    @patch('plyer.notification.notify')
    def test_notify_calls_plyer_threshold(self, mock_notify):
        title = "Test Title"
        message = "Test Message"
        notify(title, message, "threshold")
        mock_notify.assert_called_once_with(
            title="🚨 Test Title",
            message=message,
            app_name="Crypto Notifier",
            timeout=10
        )

    @patch('plyer.notification.notify')
    def test_notify_default_alert_type(self, mock_notify):
        title = "Test Title"
        message = "Test Message"
        notify(title, message)  # Should default to "movement"
        mock_notify.assert_called_once_with(
            title=title,
            message=message,
            app_name="Crypto Notifier",
            timeout=5
        )

if __name__ == "__main__":
    unittest.main() 