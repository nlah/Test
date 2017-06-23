"""
"A universal convention supplies all of maintainability,
clarity, consistency, and a foundation for good programming habits too.
What it doesn't do is insist that you follow it against your will. That's Python!"
—Tim Peters on comp.lang.python, 2001-06-16
"""
import json
import datetime
import requests
class UPC_Wolmart:
    """
    Wolmart API for upc
    """
    url = 'http://api.walmartlabs.com/v1/items'
    def __init__(self, key):
        if UPC_Wolmart.check_key(key):
            self.key = key
        else:
            raise Exception('UPC_Wolmart key')
    def elem(self, JSON_W, name):
        try:
            if name == 'date_modified':
                return  datetime.datetime.now()
            else:
                return  JSON_W[name]
        except:
            return -1

    def dict_data(self, JSON_W):
        out = {}
        for i in self.get_header_UPC():
            out[i] = self.elem(JSON_W, i)
        return out

    def get(self, upc):
        payload = {'apiKey': self.key, 'upc': upc}
        data = requests.get(self.url, params=payload, allow_redirects=False)
        data = json.loads(data.text)
        try:
            return self.dict_data(data['items'][0])
        except KeyError:
            return -1

    def update(self, mongo):
        for i in mongo.UPC.find():
            data = self.get(i['upc'])
            if data != -1:
                data['Update_time'] = datetime.datetime.now()
                mongo.UPC.update({'_id':i['_id']}, data, True)
    @staticmethod
    def check_key(key):
        payload = {'apiKey': key, 'upc': '035000521019'}
        data = requests.get('http://api.walmartlabs.com/v1/items',\
         params=payload, allow_redirects=False)
        try:
            data = json.loads(data.text)
            return (False, True)['items' in data]
        except:
            return False
    @staticmethod
    def get_header_UPC():
        return ['upc', 'salePrice', 'name', 'brandName', 'modelNumber',\
         'largeImage', 'stock', 'freeShippingOver50Dollars', 'date_modified']
