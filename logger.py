import os
import json
import logging
from logging.config import dictConfig

try:
    from pythonjsonlogger import jsonlogger
    JSONLOGGER_AVAILABLE = True
except Exception:
    JSONLOGGER_AVAILABLE = False

LOG_PATH = os.getenv("LOG_PATH", "log")
LOG_JSON = os.getenv("LOG_JSON", "true").lower() in ("1", "true", "yes")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

MAX_BYTES = int(os.getenv("LOG_MAX_BYTES", "10485760"))  # 10MB
BACKUP_COUNT = int(os.getenv("LOG_BACKUP_COUNT", "10"))

os.makedirs(LOG_PATH, exist_ok=True)


class TraceContextFilter(logging.Filter):
    """
    Custom logging filter to augment log records with trace and span
    identifiers.

    This filter ensures that every log record handled by this filter
    contains the attributes `trace_id` and `span_id`. If these attributes
    are not already present, they will be set to `None`.

    :ivar name: Name of the logging filter.
    :type name: str
    """
    def filter(self, record):
        if not hasattr(record, "trace_id"):
            record.trace_id = None

        if not hasattr(record, "span_id"):
            record.span_id = None

        return True


class SimpleJsonFormatter(logging.Formatter):
    """
    Formats log records into a JSON-formatted string.

    This class extends the logging.Formatter to produce log records in JSON format.
    It includes standard log record information such as timestamp, log level, logger
    name, and additional optional attributes like trace and span IDs for distributed
    tracing. Any extra attributes attached to the log record, not part of the standard
    log fields, are included in an "extra" section.

    :ivar default_msec_format: Default format for representing milliseconds in
        timestamps.
    :type default_msec_format: str
    """
    def format(self, record):
        message = record.getMessage()
        base = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "funcName": record.funcName,
            "lineno": record.lineno,
            "message": message,
            "pathname": record.pathname,
            "process": record.process,
            "thread": record.thread,
            "trace_id": getattr(record, "trace_id", None),
            "span_id": getattr(record, "span_id", None),
        }

        extras = {
            k: v for k, v in record.__dict__.items()
            if k not in (
                "name", "msg", "args", "levelname", "levelno", "pathname",
                "filename", "module", "exc_info", "exc_text", "stack_info",
                "lineno", "funcName", "created", "msecs", "relativeCreated",
                "thread", "threadName", "processName", "process", "message",
                "trace_id", "span_id"
            )
        }
        if extras:
            base["extra"] = extras
        return json.dumps(base, default=str, ensure_ascii=False)


def build_config():
    if JSONLOGGER_AVAILABLE:
        json_formatter = {
            "()": jsonlogger.JsonFormatter,
            "fmt": "%(asctime)s %(levelname)s %(name)s %(message)s %(trace_id)s %(span_id)s"
        }
    else:
        json_formatter = {
            "()": SimpleJsonFormatter
        }

    human_formatter = {
        "format": "[%(asctime)s] %(levelname)-4s %(funcName)s() L%(lineno)-4d %(message)s"
    }

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "filters": {
            "trace": {
                "()": TraceContextFilter
            }
        },
        "formatters": {
            "default": human_formatter,
            "json": json_formatter,
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "json" if LOG_JSON else "default",
                "stream": "ext://sys.stdout",
                "filters": ["trace"],
            },
            "detailed_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "json" if LOG_JSON else "default",
                "filename": os.path.join(LOG_PATH, "app.detailed.log"),
                "maxBytes": MAX_BYTES,
                "backupCount": BACKUP_COUNT,
                "encoding": "utf-8",
                "delay": True,
                "filters": ["trace"],
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "json" if LOG_JSON else "default",
                "filename": os.path.join(LOG_PATH, "app.error.log"),
                "level": "ERROR",
                "maxBytes": MAX_BYTES,
                "backupCount": BACKUP_COUNT,
                "encoding": "utf-8",
                "delay": True,
                "filters": ["trace"],
            },
            "debug_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "json" if LOG_JSON else "default",
                "filename": os.path.join(LOG_PATH, "app.debug.log"),
                "level": "DEBUG",
                "maxBytes": MAX_BYTES,
                "backupCount": BACKUP_COUNT,
                "encoding": "utf-8",
                "delay": True,
                "filters": ["trace"],
            }
        },
        "root": {
            "handlers": ["console", "detailed_file"],
            "level": LOG_LEVEL,
        },
        "loggers": {
            "gunicorn.error": {
                "handlers": ["console", "error_file"],
                "level": LOG_LEVEL,
                "propagate": False,
            }
        }
    }


dictConfig(build_config())

logger = logging.getLogger(__name__)
