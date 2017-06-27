# -*- coding: utf-8 -*-
from celery.schedules import crontab
# flask core settings
DEBUG = True
TESTING = False
SECRET_KEY = 'qh\x98\xc4o\xc4]\x8f\x8d\x93\xa4\xec\xc5\xfd]\xf8\xb1c\x84\x86\xa7A\xcb\xc0'
PERMANENT_SESSION_LIFETIME = 60 * 60 * 24 * 30

# flask wtf settings



# flask mongoengine settings
MONGODB_DB = 'WolmartDB'
MONGODB_HOST='127.0.0.1'
MONGODB_PORT=27017
MONGO_URI = 'mongodb://localhost:27017'
# project settings
PROJECT_FILE_NAME_SETTING=__name__
PROJECT_PASSWORD_HASH_METHOD = 'pbkdf2:sha1'
PROJECT_SIGNUP_TOKEN_MAX_AGE = 60 * 60 * 24 * 7  # in seconds
PROJECT_RECOVER_PASSWORD_TOKEN_MAX_AGE = 60 * 60 * 24 * 7  # in seconds

SESSION_TYPE = 'filesystem'
# celery settings
CELERY_WALMART_KEY = '3ayec4g84mbybsmhr3des5t6' 
BROKER_URL = 'mongodb://localhost:27017/jobs'

CELERY_RESULT_BACKEND = "mongodb"
CELERY_MONGODB_BACKEND_SETTINGS = {
    "host": "127.0.0.1",
    "port": 27017,
    "database": "jobs", 
    "taskmeta_collection": "stock_taskmeta_collection",
}


CELERYBEAT_SCHEDULE = {
    "runs-every-60-minute": {
        "task": "celery_my.tasks.add",
        "schedule": crontab(minute='*/2'),
        "args": ()
    },
}
