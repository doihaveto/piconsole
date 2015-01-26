INSTALLED_APPS = [
    'pcpower',
]

LOGGING = {
    'version': 1,
    'piconsole': {
        'level': 'DEBUG',
        'handlers': ['file'],
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'filename': 'logs/log.log',
            'maxBytes': 1024 * 1024 * 10,
            'backupCount': 50,
        }
    },
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(name)s - %(levelname)-8s - %(message)s',
        },
    },
}
