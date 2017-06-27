"""
"A universal convention supplies all of maintainability,
clarity, consistency, and a foundation for good programming habits too.
What it doesn't do is insist that you follow it against your will. That's Python!"
—Tim Peters on comp.lang.python, 2001-06-16
"""
import datetime
from flask_mongoengine import MongoEngine

db = MongoEngine()

class WalmartModel(db.Document):
    """Collection walmart data"""

    upc = db.StringField(required=True, unique=True)
    salePrice = db.DecimalField()
    name = db.StringField()
    brandName = db.StringField()
    modelNumber = db.StringField()
    largeImage = db.StringField()
    stock = db.StringField()
    freeShippingOver50Dollars = db.BooleanField(required=True)
    date_modified = db.DateTimeField(default=datetime.datetime.now)

class UserModel(db.Document):
    """Collection Users data"""

    email = db.StringField(required=True, unique=True)
    pw_hash = db.StringField(required=True)
    key = db.StringField()

    @property
    def is_authenticated(self):
        """ """

        return True

    def is_active(self):
        """ """

        return True

    def is_anonymous(self):
        """ """

        return False
        
    def get_id(self):
        """ """

        return self.email
