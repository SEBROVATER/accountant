import logging.config
from abc import ABC
from logging import FileHandler, Logger
from pathlib import Path

from general_utils.utils import get_base_dir, is_in_debug


def get_logger(name: str, with_file: bool = False, subpath: str = "."):
    debug = is_in_debug()
    if debug and not name.startswith("dev."):
        name = f"dev.{name}"

    if with_file:
        log_path = get_base_dir() / "logs" / subpath.strip("/")
        log_path = log_path / f"{name}.log"
        log_path.parent.mkdir(exist_ok=True)

    level = "DEBUG" if debug else "INFO"

    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "[{asctime}] {levelname:^7} | def {funcName}() | {message}",
                "style": "{",
            },
        },
        "handlers": {
            "console": {
                "level": level,
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
        },
        "root": {
            "level": "DEBUG",
        },
        "loggers": {
            name: {
                "handlers": ["file", "console"] if with_file else ["console"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }
    if with_file:
        config["handlers"].update(
            {
                "file": {
                    "level": "DEBUG",
                    "class": "logging.FileHandler",
                    "filename": log_path.as_posix(),
                    "encoding": "utf-8",
                    "formatter": "verbose",
                },
            }
        )
    logging.config.dictConfig(config)

    return logging.getLogger(name)


class GeneralLogging(ABC):
    logger: Logger

    @classmethod
    def debug(cls, *args, **kwargs):
        cls.logger.debug(*args, **kwargs)

    @classmethod
    def info(cls, *args, **kwargs):
        cls.logger.info(*args, **kwargs)

    @classmethod
    def warning(cls, *args, **kwargs):
        cls.logger.warning(*args, **kwargs)

    @classmethod
    def error(cls, *args, **kwargs):
        cls.logger.error(*args, **kwargs)

    @classmethod
    def exception(cls, *args, **kwargs):
        cls.logger.exception(*args, **kwargs)

    @classmethod
    def critical(cls, *args, **kwargs):
        cls.logger.critical(*args, **kwargs)

    @classmethod
    def close(cls):
        for handler in cls.logger.handlers:
            handler.close()

    @classmethod
    def log_path(cls) -> Path | None:
        for handler in cls.logger.handlers:
            if isinstance(handler, FileHandler):
                return Path(handler.baseFilename)

    @classmethod
    def replace_logger(cls, with_file: bool, sub_path: str = "."):
        name = cls.logger.name
        cls.close()
        cls.logger = get_logger(name, with_file=with_file, subpath=sub_path)
