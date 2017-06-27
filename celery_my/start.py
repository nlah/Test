"""
"A universal convention supplies all of maintainability,
clarity, consistency, and a foundation for good programming habits too.
What it doesn't do is insist that you follow it against your will. That's Python!"
—Tim Peters on comp.lang.python, 2001-06-16
"""
from  . tasks import app

def worker_start():
    """ start worker """

    app.start(argv=['celery', 'worker'])

def beat_start():
    """ start beat """

    app.start(argv=['celery', 'beat', '-l', 'info'])
