import logging
from pprint import pformat

class Logger:
    def __init__(self, log_level=logging.DEBUG):
        """
        Initializes a Logger instance.

        Args:
          log_level (int, optional): The logging level. Defaults to logging.DEBUG.
        """
        self.logger = logging.getLogger("Andiran-Dev")
        self.logger.setLevel(log_level)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def debug(self, message, *args, **kwargs):
        """
        Logs a debug message with optional arguments for formatting.

        Args:
          message (str): The message to log.
          *args: Additional arguments for formatting the message using f-strings.
          **kwargs: Keyword arguments for formatting the message using f-strings.
        """
        formatted_message = message.format(*args, **kwargs)
        #self.logger.debug(formatted_message)
        print(pformat(formatted_message))

    def info(self, message, *args, **kwargs):
        """
        Logs an informational message with optional arguments for formatting.

        Args:
          message (str): The message to log.
          *args: Additional arguments for formatting the message using f-strings.
          **kwargs: Keyword arguments for formatting the message using f-strings.
        """
        self.logger.info(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        """
        Logs a warning message with optional arguments for formatting.

        Args:
          message (str): The message to log.
          *args: Additional arguments for formatting the message using f-strings.
          **kwargs: Keyword arguments for formatting the message using f-strings.
        """
        self.logger.warning(message, *args, **kwargs)

    def error(self, message, *args, **kwargs):
        """
        Logs an error message with optional arguments for formatting.

        Args:
          message (str): The message to log.
          *args: Additional arguments for formatting the message using f-strings.
          **kwargs: Keyword arguments for formatting the message using f-strings.
        """
        formatted_message = message.format(*args, **kwargs)
        #self.logger.error(formatted_message)
        print(pformat(formatted_message))

    def critical(self, message, *args, **kwargs):
        """
        Logs a critical message with optional arguments for formatting.

        Args:
          message (str): The message to log.
          *args: Additional arguments for formatting the message using f-strings.
          **kwargs: Keyword arguments for formatting the message using f-strings.
        """
        self.logger.critical(message, *args, **kwargs)

    def set_level(self, level):
        """
        Sets the logging level for the logger.

        Args:
          level (int): The new logging level.
        """
        self.logger.setLevel(level)