# -*- coding: utf-8 -*-
from celery.schedules import crontab
# flask core settings
DEBUG = True
TESTING = False
SECRET_KEY = 'qh\x98\xc4o\xc4]\x8f\x8d\x93\xa4\xec\xc5\xfd]\xf8\xb1c\x84\x86\xa7A\xcb\xc0'
PERMANENT_SESSION_LIFETIME = 60 * 60 * 24 * 30

# flask wtf settings

# flask mongoengine settings


# flask mail settings



# project settings
PROJECT_FILE_NAME_SETTING=__name__

PROJECT_PASSWORD_HASH_METHOD = 'pbkdf2:sha1'
PROJECT_SITE_NAME = u'Flask Example'
PROJECT_SITE_URL = u'http://127.0.0.1:5000'
PROJECT_SIGNUP_TOKEN_MAX_AGE = 60 * 60 * 24 * 7  # in seconds
PROJECT_RECOVER_PASSWORD_TOKEN_MAX_AGE = 60 * 60 * 24 * 7  # in seconds

MONGO_URI = 'mongodb://localhost:27017'
SESSION_TYPE = 'filesystem'

CELERY_BROKER_URL = 'mongodb://localhost:27017/jobs'

CELERY_RESULT_BACKEND = "mongodb"
CELERY_MONGODB_BACKEND_SETTINGS = {
    "host": "127.0.0.1",
    "port": 27017,
    "database": "jobs", 
    "taskmeta_collection": "stock_taskmeta_collection",
}
CELERY_IMPORTS=("task",)


CELERYBEAT_SCHEDULE = {
    "runs-every-60-minute": {
        "task": "task.add",
        "schedule": crontab(minute='*/60'),
        "args": ()
    },
}
