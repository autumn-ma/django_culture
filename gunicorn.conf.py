import multiprocessing
import sys

# Server socket
bind = "0.0.0.0:8001"
backlog = 2048

# Worker processes
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 300
keepalive = 2

# Logging
accesslog = "/var/log/culture/web-access.log"
errorlog = "/var/log/culture/web-error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Custom logging configuration to enable dual output (file + stdout/stderr)
logconfig_dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "generic": {
            "format": "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter"
        },
        "access": {
            "format": '%(message)s',
            "class": "logging.Formatter"
        }
    },
    "handlers": {
        "console_error": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stderr
        },
        "console_access": {
            "class": "logging.StreamHandler",
            "formatter": "access",
            "stream": sys.stdout
        },
        "error_file": {
            "class": "logging.FileHandler",
            "formatter": "generic",
            "filename": "/var/log/culture/web-error.log"
        },
        "access_file": {
            "class": "logging.FileHandler",
            "formatter": "access",
            "filename": "/var/log/culture/web-access.log"
        }
    },
    "loggers": {
        "gunicorn.error": {
            "level": "INFO",
            "handlers": ["console_error", "error_file"],
            "propagate": False,
            "qualname": "gunicorn.error"
        },
        "gunicorn.access": {
            "level": "INFO",
            "handlers": ["console_access", "access_file"],
            "propagate": False,
            "qualname": "gunicorn.access"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console_error"]
    }
}
