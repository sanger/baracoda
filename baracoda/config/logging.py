LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "colored": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(asctime)-15s %(name)-18s:%(lineno)s %(log_color)s%(levelname)-5s %(message)s",
        },
        "verbose": {"format": "%(asctime)-15s %(name)-18s:%(lineno)s %(levelname)-5s %(message)s"},
    },
    "handlers": {
        "colored_stream": {
            "level": "DEBUG",
            "class": "colorlog.StreamHandler",
            "formatter": "colored",
        },
        "slack": {
            "level": "ERROR",
            "class": "baracoda.utils.SlackHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {"baracoda": {"handlers": ["colored_stream", "slack"], "level": "DEBUG", "propagate": True}},
}
