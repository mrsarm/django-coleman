# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See https://docs.djangoproject.com/en/3.2/topics/logging/ for
# more details on how to customize your logging configuration.

from . import env

LOG_LEVEL = env('LOG_LEVEL', 'INFO')
LOG_LEVEL_DJANGO = env('LOG_LEVEL_DJANGO', LOG_LEVEL)
LOG_LEVEL_DJANGO_DB = env('LOG_LEVEL_DJANGO_DB', LOG_LEVEL)
LOG_LEVEL_DJANGO_REQ = env('LOG_LEVEL_DJANGO_REQ', LOG_LEVEL_DJANGO)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            #'format': '%(levelname)s %(asctime)s [%(name)s] %(process)d %(thread)d %(message)s',
            'format': '%(asctime)s %(levelname)s [%(name)s] %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': "app.log",
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'verbose',
        },
        # 'mail_admins': {
        #     'level': 'ERROR',
        #     'class': 'django.utils.log.AdminEmailHandler'
        # }
    },
    'loggers': {
        'django.request': {
            'handlers': ['console', 'logfile'],
            'level': LOG_LEVEL_DJANGO_REQ,
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console', 'logfile'],
            'propagate': False,
            'level': LOG_LEVEL_DJANGO_DB,
        },
        'django': {
            'handlers': ['console', 'logfile'],
            'propagate': True,
            'level': LOG_LEVEL_DJANGO,
        },
        '': {
            'handlers': ['console', 'logfile'],
            'level': LOG_LEVEL,
        },
    }
}
