
"""
"A universal convention supplies all of maintainability,
clarity, consistency, and a foundation for good programming habits too.
What it doesn't do is insist that you follow it against your will. That's Python!"
—Tim Peters on comp.lang.python, 2001-06-16
"""
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
