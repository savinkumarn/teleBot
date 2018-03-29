import requests
import threading

smileface = u'\U0001F601'
sadface = u'\U0001F641'
neutralface = u'\U0001F928'

url = "https://api.coinmarketcap.com/v1/ticker/"
convert = "/?convert=INR&limit=200"

class cryptoClass():
    '''
    This class is used to create a report class
    '''
    def __init__(self, response, master_data):
        self.response = response
        self.master_data = master_data

    def prepare_master_data(self):
        for i in self.response:
            resp = ''
            resp = resp + i['symbol'] + ' $'
            resp = resp + i['price_usd'] + ' INR '
            resp = resp + str('{:.2f}'.format(float(i['price_inr']))) + ' '
            resp = resp + i['percent_change_1h'] + '% '
            if float(i['percent_change_1h']) > 0:
                resp = resp + smileface
            else:
                resp = resp + sadface
            self.master_data[i['symbol'].upper()] = resp

    def get_response_from_api(self):
        threading.Timer(300, self.get_response_from_api).start()
        params = {'timeout': 100, 'offset': None}
        self.response = requests.get(url + convert, data=params).json()
        self.prepare_master_data()

    def get_coin_data_from_api(self, req):
        try:
            ret = self.master_data[req]
        except KeyError:
            ret = req + ' not found' + neutralface
        return ret