"""
"A universal convention supplies all of maintainability,
clarity, consistency, and a foundation for good programming habits too.
What it doesn't do is insist that you follow it against your will. That's Python!"
—Tim Peters on comp.lang.python, 2001-06-16
"""
import os
import sys
sys.path.append(os.path.dirname(__name__))
from manager import Manager
from walmart_upc import create_app
from celery_my.start import worker_start,beat_start

manager = Manager()

@manager.command
def runserver():
    """ """

    app = create_app()
    app.run(debug=True)

@manager.command
def run_worker():
    """ """

    worker_start()

@manager.command
def run_beat():
    """ """

    beat_start()
if __name__ == '__main__':
    manager.main()

