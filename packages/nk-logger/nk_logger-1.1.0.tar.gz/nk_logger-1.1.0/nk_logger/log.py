""" Sets up logging config for stream handlers sending info-level logs and
below to stdout and warning-level and above to stderr, provides get_logger
function. Designed to work well with datadog. """

import logging
import os
import sys

from pythonjsonlogger import jsonlogger

LOG_LEVEL_STR2INT = {
    "CRITICAL": 50,
    "ERROR": 40,
    "WARNING": 30,
    "INFO": 20,
    "DEBUG": 10,
    "NOTSET": 0,
}


LOGGER_CONFIG = {"level": "INFO", "prefix": ""}


def update_config(prefix=None, level=None):
    """ update default logger config values with any provided, converting level from string to int if needed """
    level = level if level else LOGGER_CONFIG["level"]

    if isinstance(level, str):
        # convert string form to int for comparisons
        level = LOG_LEVEL_STR2INT[level]
    LOGGER_CONFIG["level"] = level

    if prefix:
        LOGGER_CONFIG["prefix"] = prefix


def config_logger(prefix=None, level=None, root_log_level=None, formatter=None):
    """ Initialize the datadog-friendly log handlers and attach them to the
    root logger (after removing any previous loggers already attached). If
    provided, `prefix` and `level` set log level and logger name prefix
    values in LOGGER_CONFIG which sets the default for loggers returned by
    get_logger. the root logger is given the same log level as the handlers
    unless `root_log_level` is provided, in which case it is set to that
    value instead. """

    if not formatter:
        formatter = jsonlogger.JsonFormatter(timestamp=True, reserved_attrs=[])

    # out_handler writes to stdout and handles logs of log level 'INFO' and below
    out_handler = logging.StreamHandler(sys.stdout)
    out_handler.setFormatter(formatter)
    out_handler.addFilter(lambda record: record.levelno < logging.WARNING)

    # err_handler writes to stderr and handles logs of level max('WARNING', `level`) and above
    err_handler = logging.StreamHandler(sys.stderr)
    err_handler.setFormatter(formatter)

    # set log config defaults with level and prefix if provided
    update_config(prefix=prefix, level=level)

    # set log level for err and out handlers
    err_log_level = max(logging.WARNING, LOGGER_CONFIG["level"])
    err_handler.setLevel(err_log_level)
    out_handler.setLevel(LOGGER_CONFIG["level"])

    # set root logger level to same as handlers unless root_log_level is provided
    root = logging.getLogger()
    root_log_level = root_log_level if root_log_level else LOGGER_CONFIG["level"]
    root.setLevel(root_log_level)

    # remove any present handlers, then add err and out handlers to root logger
    root.handlers = []
    root.addHandler(out_handler)
    root.addHandler(err_handler)


def get_logger(name, prefix=None, level=None):
    """ Returns a logger object with given `name` prefixed with `prefix` and log
    level `level`. If level or prefix aren't provided, they are set to
    LOGGER_CONFIG defaults. """
    level = level if level else LOGGER_CONFIG["level"]
    prefix = prefix if prefix else LOGGER_CONFIG["prefix"]

    logger_name = f"{prefix}.{name}" if prefix else name
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    return logger


# update default config values with env vars if provided
update_config(level=os.getenv("LOG_LEVEL"), prefix=os.getenv("SERVICE_NAME"))
config_logger()  # configure logger with default values

_logger = get_logger(__name__)
_logger.info("logger initialized")
