"""
"A universal convention supplies all of maintainability,
clarity, consistency, and a foundation for good programming habits too.
What it doesn't do is insist that you follow it against your will. That's Python!"
—Tim Peters on comp.lang.python, 2001-06-16
"""
import json
import datetime
import requests
class UpcWalmart(object):
    """Walmart API for upc"""

    url = 'http://api.walmartlabs.com/v1/items'
    def __init__(self, key):
        if UpcWalmart.check_key(key):
            self.key = key
        else:
            raise Exception('UpcWalmart key')

    def elem(self, json_w, name):
        """



        Args:

          json_w: 

          name: 



        Returns:
            


        """

        try:
            if name == 'date_modified':
                return  datetime.datetime.now()
            return  json_w[name]
        except:
            return -1

    def dict_data(self, json_w):
        """



        Args:

          json_w: 



        Returns:

        dict with data about product

        """

        out = {}
        for i in self.get_header_upc():
            out[i] = self.elem(json_w, i)
        return out

    def get(self, upc):
        """



        Args:

          upc: 



        Returns:
            dict with data about product


        """

        payload = {'apiKey': self.key, 'upc': upc}
        data = requests.get(self.url, params=payload, allow_redirects=False)
        data = json.loads(data.text)
        try:
            data = self.dict_data(data['items'][0])
            data['modelNumber'] = str(data['modelNumber'])
            return data
        except KeyError:
            return -1

    def update(self, mongo):
        """
            


        Args:

          mongo: 



        Returns:



        """

        for i in mongo.walmart_model.find():
            data = self.get(i['upc'])
            if data != -1:
                data['date_modified'] = datetime.datetime.now()
                mongo.walmart_model.update({'_id':i['_id']}, data, True)

    @staticmethod
    def check_key(key):
        """



        Args:

          key: 



        Returns:

            False, True

        """

        payload = {'apiKey': key, 'upc': '035000521019'}
        data = requests.get('http://api.walmartlabs.com/v1/items',\
         params=payload, allow_redirects=False)
        try:
            data = json.loads(data.text)
            return (False, True)['items' in data]
        except:
            return False

    @staticmethod
    def get_header_upc():
        """ Returnning list of walmart keys name """

        return ['upc', 'salePrice', 'name', 'brandName', 'modelNumber',\
         'largeImage', 'stock', 'freeShippingOver50Dollars', 'date_modified']

