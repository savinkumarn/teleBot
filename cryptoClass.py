from base64 import _85encode

import requests
import threading
import datetime

smileface = u'\U0001F601'
sadface = u'\U0001F641'
neutralface = u'\U0001F928'

url = "https://api.coinmarketcap.com/v1/ticker/"
convert = "/?convert=INR&limit=200"
#response ="{[{'id': 'bitcoin', 'name': 'Bitcoin', 'symbol': 'BTC', 'rank': '1', 'price_usd': '7450.18', 'price_btc': '1.0', '24h_volume_usd': '4867730000.0', 'market_cap_usd': '126103512373', 'available_supply': '16926237.0', 'total_supply': '16926237.0', 'max_supply': '21000000.0', 'percent_change_1h': '-3.16', 'percent_change_24h': '-7.24', 'percent_change_7d': '-19.11', 'last_updated': '1521383065', 'price_inr': '484820.4635', '24h_volume_inr': '316767529750.0000000000', 'market_cap_inr': '8206186067651'}]}"

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
        threading.Timer(3000, self.get_response_from_api).start()
        params = {'timeout': 100, 'offset': None}
        self.response = requests.get(url + convert, data=params).json()
        self.prepare_master_data()

    def get_coin_data_from_api(self, req):
        try:
            ret = self.master_data[req]
        except KeyError:
            ret = req +' not found'+neutralface
        return ret