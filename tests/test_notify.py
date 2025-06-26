import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import unittest
from unittest.mock import patch
from notifier.runner import notify

class TestNotify(unittest.TestCase):
    @patch('plyer.notification.notify')
    def test_notify_calls_plyer(self, mock_notify):
        title = "Test Title"
        message = "Test Message"
        notify(title, message)
        mock_notify.assert_called_once_with(
            title=title,
            message=message,
            app_name="Crypto Notifier",
            timeout=5
        )

if __name__ == "__main__":
    unittest.main() 