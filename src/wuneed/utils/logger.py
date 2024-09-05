import logging
import os
from logging.handlers import RotatingFileHandler
from typing import Dict, Any

class WuneedLogger:
    def __init__(self):
        self.logger = logging.getLogger("wuneed")
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler("wuneed.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_command(self, command: str, args: Dict[str, Any]):
        self.logger.info(f"Command executed: {command} with args: {args}")

    def log_plugin_usage(self, plugin_name: str, context: Dict[str, Any]):
        self.logger.info(f"Plugin used: {plugin_name} with context: {context}")

wuneed_logger = WuneedLogger()

def setup_logger(name: str, log_file: str, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger

main_logger = setup_logger('wuneed', 'logs/wuneed.log')