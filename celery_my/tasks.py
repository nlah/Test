import os
import time 
from datetime import timedelta
from pymongo import MongoClient
from walmart_upc. upc import UpcWalmart
from . celery_app import app
@app.task
def add():
    """
    Update the database on upc
    """
    wolmart = UpcWalmart(app.conf['CELERY_WALMART_KEY'])
    client = MongoClient(app.conf['MONGO_URI'])
    wolmart.update(client[app.conf['MONGODB_DB']])
