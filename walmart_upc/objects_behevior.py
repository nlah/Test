"""
"A universal convention supplies all of maintainability,
clarity, consistency, and a foundation for good programming habits too.
What it doesn't do is insist that you follow it against your will. That's Python!"
—Tim Peters on comp.lang.python, 2001-06-16
"""
import io
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash
from walmart_upc.upc import UpcWalmart
from walmart_upc.model import UserModel, WalmartModel

class User():
    """
       Object to interact user and db
    """

    url = 'http://api.walmartlabs.com/v1/items'

    @staticmethod
    def get_user(username=None, password=None):
        """

            

        Args:

          username:  (Default value = None)

          password:  (Default value = None)



        Returns:

            User if exist

        """

        user = UserModel.objects.get(email=username)
        if check_password_hash(user.pw_hash, password) != True:
            raise Exception('password')
        else:
            return   user

    def __init__(self, user: UserModel):
        self.user = user
        try:
            self.user_upc = UpcWalmart(self.user.key)
        except Exception as err:
            self.user_upc = err.args

    def set_key(self, key:str):
        """

            Initing key Walmart

        Args:

          key: str: 



        Returns:



        """

        if  UpcWalmart.check_key(key):
            self.user.key = key
            UserModel.objects(email=self.user.email, pw_hash=self.user.pw_hash).\
             update_one(set__key=key, upsert=True)
            self.user_upc = UpcWalmart(self.user.key)

    def  key_walmart(self):
        """ Return key Walmart if exist """

        if isinstance(self.user_upc, UpcWalmart):
            return self.user_upc.key
        else:
            return "key Error"

    def set_upc(self, upc):
        """



        Args:

          upc: 



        Returns:

            -1  if not add in db
             1 if add in db
             self.user_upc if  self.user_upc not UpcWalmart object
        """

        if isinstance(self.user_upc, UpcWalmart):
            try:
                WalmartModel.objects.get(upc=upc)
                return -1
            except WalmartModel.DoesNotExist:
                data = self.user_upc.get(upc)
                try:
                    WalmartModel(**data).save()
                except TypeError:
                    return -1
            return 1
        else:
            return self.user_upc

    def get_upc(self):
        """ """

        return [i.to_mongo() for i in WalmartModel.objects]

    def get_upc_limit_sort(self, start, end, key, sort_type):
        """



        Args:

          start: 

          end: 

          key: 

          sort_type: 



        Returns:

            

        """

        key = ('+' + key, '-' + key)[sort_type == 1]
        return [i.to_mongo() for i in WalmartModel.objects.order_by(key)[start:start+end]]

    def get_csv(self):
        """ Return csv file """

        csv_data = []
        column_name = self.user_upc.get_header_UPC()
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
        """

        Add upc from csv in db

        Args:

          file_data: 



        Returns:

            list of not added keys

        """

        try:
            df = pd.read_csv(io.StringIO(file_data.decode('utf-8')), dtype={'upc':str})['upc']
        except KeyError:
            return -1
        out = []
        for i in df:
            if self.set_upc(i) == -1:
                out.append(i)
        return out

    def del_upc(self, upc: str):
        """

        Delete upc from db

        Args:

          upc: str: 



        Returns:

            

        """

        return WalmartModel.objects(upc=upc).delete()

    def count_upc(self):
        """ Coutn upc in db """

        return WalmartModel.objects.count()

class UserGenerate(object):
    """ Object for generete user """

    def __init__(self, username, password, password_test):
        if password != password_test:
            raise Exception('passwords not equal')
        self.username = username
        self.set_password(password)
        UserModel(email=self.username, pw_hash=self.pw_hash).save()

    def set_password(self, password):
        """



        Args:

          password: 



        Returns:



        """

        self.pw_hash = generate_password_hash(password)
        
    def to_dict(self):
        """  """

        return {'email':self.username, 'pw_hash':self.pw_hash}

