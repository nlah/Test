"""
It is alive
"""
import datetime
from flask_mongoengine import MongoEngine

db = MongoEngine()

class wolmart_model(db.Document):
    """
    It is alive
    """

    upc = db.StringField(required=True, unique=True)
    salePrice = db.DecimalField()
    name = db.StringField()
    brandName = db.StringField()
    modelNumber = db.StringField()
    largeImage = db.StringField()
    stock = db.StringField()
    freeShippingOver50Dollars = db.BooleanField(required=True)
    date_modified = db.DateTimeField(default=datetime.datetime.now)

class user_model(db.Document):
    """
    It is alive
    """
    email = db.StringField(required=True, unique=True)
    pw_hash = db.StringField(required=True)
    key = db.StringField()

    @property
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.email





