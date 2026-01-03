"""Structured JSON logging configuration"""

import logging
import sys
from pythonjsonlogger import jsonlogger


def setup_logging(service_name: str, log_level: str = "INFO"):
    """Configure structured JSON logging"""
    logger = logging.getLogger()
    logger.setLevel(log_level)

    handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        "%(timestamp)s %(level)s %(name)s %(message)s",
        rename_fields={"levelname": "level", "asctime": "timestamp"}
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    logger.info(f"{service_name} logging configured at {log_level} level")
    return logger
