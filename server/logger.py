from threading import Lock
import logging
from logging.handlers import RotatingFileHandler
import os


class Logger:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Logger, cls).__new__(cls)
                    cls._instance._initialize()   
        return cls._instance

    def _initialize(self):
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file = os.path.join(log_dir, "app.log")
        self.logger = logging.getLogger("my_app_logger")
        self.logger.setLevel(logging.INFO)
        if not self.logger.handlers:

            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=5_000_000,
                backupCount=5
            )
            file_formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(module)s | %(message)s"
            )
            file_handler.setFormatter(file_formatter)
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter("%(levelname)s | %(message)s")
            console_handler.setFormatter(console_formatter)
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger
