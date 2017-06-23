"""
"A universal convention supplies all of maintainability,
clarity, consistency, and a foundation for good programming habits too.
What it doesn't do is insist that you follow it against your will. That's Python!"
—Tim Peters on comp.lang.python, 2001-06-16
"""
import io
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
from sample_application.upc import UPC_Wolmart
from sample_application.model import user_model, wolmart_model

class User():
    """
    It is alive
    """
    url = 'http://api.walmartlabs.com/v1/items'
    @staticmethod
    def get_user(username=None, password=None):
        user = user_model.objects.get(email=username)
        if check_password_hash(user.pw_hash, password) != True:
            raise Exception('password')
        else:
            return   user

    def __init__(self, user: user_model):
        self.user = user
        try:
            self.User_UPC = UPC_Wolmart(self.user.key)
        except Exception as err:
            self.User_UPC = err.args


    def set_key(self, key):
        if  UPC_Wolmart.check_key(key):
            self.user.key = key
            user_model.objects(email=self.user.email, pw_hash=self.user.pw_hash).\
             update_one(set__key=key, upsert=True)
            self.User_UPC = UPC_Wolmart(self.user.key)
    def  key_wolmart(self):
        if isinstance(self.User_UPC, UPC_Wolmart):
            return self.User_UPC.key
        else:
            return "key Error"
    def set_upc(self, upc):
        if isinstance(self.User_UPC, UPC_Wolmart):
            try:
                wolmart_model.objects.get(upc=upc)
                return 1
            except wolmart_model.DoesNotExist:
                data = self.User_UPC.get(upc)
                if data != 1:
                    wolmart_model(**data).save()
                else:
                    return -1
            return 1
        else:
            return self.User_UPC

    def get_upc(self):
        return [i.to_mongo() for i in wolmart_model.objects]

    def get_upc_limit_sort(self, start, end, key, sort_type):
        key = ('+' + key, '-' + key)[sort_type == 1]
        return [i.to_mongo() for i in wolmart_model.objects.order_by(key)[start:start+end]]

    def get_csv(self):
        csv_data = []
        column_name = self.User_UPC.get_header_UPC()
        for i in column_name:
            csv_data.append([])
        for i in self.get_upc():
            for j in range(len(column_name)):
                try:
                    csv_data[j].append(i[column_name[j]])
                except:
                    csv_data[j].append(-1)
        df = pd.DataFrame(csv_data).transpose()
        df.columns = column_name
        return df.to_csv(index=False)

    def set_csv(self, file_data):
        try:
            df = pd.read_csv(io.StringIO(file_data.decode('utf-8')), dtype={'upc':str})['upc']
        except KeyError:
            return -1
        out = {}
        for i in df:
            if self.set_upc(i) == -1:
                out[i] = -1
        return out

    def del_upc(self, upc: str):
        return wolmart_model.objects(upc=upc).delete()

    def count_upc(self):
        return wolmart_model.objects.count()

class User_generate(object):
    def __init__(self, username, password, password_test):
        if password != password_test:
            raise Exception('passwords not equal')
        self.username = username
        self.set_password(password)
        user_model(email=self.username, pw_hash=self.pw_hash).save()
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
    def to_dict(self):
        return {'email':self.username, 'pw_hash':self.pw_hash}

