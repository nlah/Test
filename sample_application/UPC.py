from __future__ import absolute_import
import requests
import json
import pandas as pd
import datetime
class UPC_Wolmart:
   def __init__(self,url,key):
        self.url=url
        self.key=key
   def elem(self,JSON_W,name):
        try:
            return  JSON_W[name]
        except:
            return -1

   def json_data(self,JSON_W):
        out={} 
        out['upc']=self.elem(JSON_W,'upc')
        out['salePrice']=int(self.elem(JSON_W,'salePrice'))
        out['name']=self.elem(JSON_W,'name')
        out['brandName']=self.elem(JSON_W,'brandName')
        out['modelNumber']=self.elem(JSON_W,'modelNumber')
        out['largeImage']=self.elem(JSON_W,'largeImage')
        out['quantity']=self.elem(JSON_W,'stock')
        out['freeShippingOver50Dollars']=self.elem(JSON_W,'freeShippingOver50Dollars')
        if self.elem(JSON_W,'quantity')=='Not available':
            out['IN_stock']=False
        else:
            out['IN_stock']=True
        out['Update_time']=datetime.datetime.now()
        return out




   @staticmethod
   def get_header_UPC():
                return ['upc','salePrice','name','brandName','modelNumber','largeImage','quantity','freeShippingOver50Dollars', 'IN_stock','Update_time']
   def get(self,upc):
        print('aaa')
        payload = {'apiKey': self.key, 'upc': upc}
        data=requests.get(self.url,params=payload,allow_redirects=False)
        data=json.loads(data.text)
        try:
            return self.json_data(data['items'][0])
        except KeyError:
            return -1
   def check_key(self,key):
        payload = {'apiKey': key, 'upc': '035000521019'}
        data=requests.get(self.url,params=payload,allow_redirects=False)
        try:
            check=data['items']
            return True
        except:
            return False


   def update(self,mongo):
        for i in mongo.UPC.find():
            data=self.get(i['upc'])
            if(data!=-1):
                data['Update_time']=datetime.datetime.now()
                mongo.UPC.update({'_id':i['_id']}, data, True) 
