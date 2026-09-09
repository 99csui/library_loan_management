import unittest
from unittest.mock import patch

from main import main


class TestMain(unittest.TestCase):

    @patch("main.ConsoleMenu")
    def test_main_starts_console_menu(self, mocked_console_menu):
        mocked_menu_instance = mocked_console_menu.return_value

        main()

        mocked_console_menu.assert_called_once()
        mocked_menu_instance.run.assert_called_once()


if __name__ == "__main__":
    unittest.main()