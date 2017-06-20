from werkzeug.security import generate_password_hash, check_password_hash
from flask_pymongo import PyMongo
from sample_application.UPC import UPC_Wolmart
import pandas as pd
import io



class User(object):
    list_upc=[]
    url='http://api.walmartlabs.com/v1/items'

    def __init__(self, username, password,db):
        self.coll=db.User
        self.db=db
        self.user=db.User.find_one({'name': username})
        self.username =username
        self.pw_hash=self.user['password']
        if (self.check_password(password))!=True :
            raise Exception('password')
        try:
           self.User_UPC=UPC_Wolmart(self.url,self.user["key"])
        except KeyError:
            self.User_UPC="key Error" 
    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)
    def set_key(self,key):
        
         if isinstance(self.User_UPC, UPC_Wolmart):
            if self.User_UPC.check_key(key):
                 self.user['key']=key
                 self.coll.update({'_id':self.user['_id']}, self.user, True) 
                 self.User_UPC=UPC_Wolmart(self.url,key)
                 self.__Wolmart_key=True
         else:
             self.user['key']=key
             self.coll.update({'_id':self.user['_id']}, self.user, True) 
             self.User_UPC=UPC_Wolmart(self.url,key)
             self.__Wolmart_key=True
    def Key_Wolmart(self):
       if isinstance(self.User_UPC, UPC_Wolmart) :
            return self.User_UPC.key
       else:
            return "key Error" 
    def set_upc(self,upc):
        if isinstance(self.User_UPC, UPC_Wolmart) :
            if self.db.UPC.find_one({'upc': upc})!=None:
                pass
            else:
                data=self.User_UPC.get(upc)
                if(data!=-1):
                    self.db.UPC.insert(data) 
                else:
                    return -1
            return 1
        else:
            return self.User_UPC

    def get_upc(self):
        out=[]
        for i in self.db.UPC.find():
            out.append(i)
        return out
    def get_upc_limit_sort(self,start,end,key,type):
        out=[]
        for i in self.db.UPC.find().sort(key,type).skip(start).limit(end):
            out.append(i)
        return out



    def get_csv(self):
        csv_data=[]
        column_name=self.User_UPC.get_header_UPC()
        Upc_data=self.get_upc()
        for i in column_name:
             csv_data.append([])  
        for i in Upc_data:
            for j in range(len(column_name)):
                try:
                    csv_data[j].append(i[column_name[j]])
                except:
                    csv_data[j].append(-1)
        print(csv_data)  
        df=pd.DataFrame(csv_data).transpose()
        df.columns = column_name
        print(df)  
        print(df.to_csv(index=False))  

        return df.to_csv(index=False)





    def set_csv(self,file_data):
        try:
            df = pd.read_csv(io.StringIO(file_data.decode('utf-8')),dtype={'upc':str})['upc']
        except KeyError:
            return -1
        out={}
        for i in df:
            if self.set_upc(i)==-1:
                out[i]  = -1
        return    out



    def del_upc(self,upc:str):
        self.db.UPC.remove({'upc': upc})








class User_generate(object):
    def __init__(self, username, password,password_test,db):
        if password!=password_test:
            raise Exception('passwords not equal') 
        self.username = username
        self.set_password(password)
        db.User.insert(self.json())
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
    def json(self):
        return {'name':self.username,'password':self.pw_hash}

class User_auth():

    def __init__(self, username):
        self.username = username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username
