from locale import currency

import requests
import threading
import customExceptions as CE

smileface = u'\U0001F601'
sadface = u'\U0001F641'
neutralface = u'\U0001F928'

url = "https://api.coinmarketcap.com/v1/ticker/"
convertINR = "/?convert=INR&limit=200"
convert = "/?convert="
params = {'timeout': 100, 'offset': None}
currency_list = ["AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK",
               "DKK", "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY",
               "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PKR", "PLN", "RUB", "SEK",
               "SGD", "THB", "TRY", "TWD", "ZAR", "USD"]

class cryptoClass():
    '''
    This class is used to create a report class
    '''
    def __init__(self):
        self.response = ''
        self.master_data = {}
        self.convert_response=''

    def validate_data(self,inputList):
        if len(inputList) < 3:
            raise CE.DataException('Not enough arguments, use /hp you fucking knob head')
        elif len(inputList) > 3:
            raise CE.DataException('What are you trying to do. use /hp before trying to fuck me')
        else :
            try:
                float(inputList[0])
                self.master_data[str(inputList[1]).upper()]
                self.master_data[str(inputList[2]).upper()]
            except ValueError:
                raise CE.DataException('I take numbers as argument not ur mum')
            except KeyError:
                if str(inputList[1]).upper() in currency_list or str(inputList[2]).upper() in currency_list:
                    return
                else :
                    raise CE.DataException('Conversion not possible with the shit coins you have given as input')

    def prepare_master_data(self):
        for i in self.response:
            inner_dict = {}
            inner_dict['id'] = i['id']
            inner_dict['symbol'] = i['symbol']
            inner_dict['price_usd'] = i['price_usd']
            inner_dict['price_inr'] = str('{:.2f}'.format(float(i['price_inr'])))
            inner_dict['percent_change_1h'] = i['percent_change_1h']
            resp = i['symbol'] + ' $' + i['price_usd'] + ' INR ' + \
                   str('{:.2f}'.format(float(i['price_inr']))) + ' ' + i['percent_change_1h'] \
                   + '% ' + (smileface if float(i['percent_change_1h']) > 0 else sadface)
            inner_dict['response'] = resp
            self.master_data[i['symbol'].upper()] = inner_dict

    def format_convert_response(self, reqList):
        if str(reqList[1]).upper() in currency_list:
            priceVar = 'price_' + str(reqList[1]).lower()
            totalConv = float(reqList[0]) / float(self.convert_response[0][priceVar])
        else:
            priceVar = 'price_' + str(reqList[2]).lower()
            totalConv = float(self.convert_response[0][priceVar]) * float(reqList[0])

        return reqList[0] + ' ' + str(reqList[1]).upper() + ' = ' \
               + str('{:.5f}'.format(totalConv)) + ' ' + str(reqList[2]).upper()

    def frame_url(self, reqList):
        if str(reqList[2]).upper() in currency_list:
            l_url = url + self.master_data[str(reqList[1]).upper()]['id'] + convert \
                    + str(reqList[2]).upper()
        elif str(reqList[1]).upper() in currency_list:
            l_url = url + self.master_data[str(reqList[2]).upper()]['id'] + convert \
                    + str(reqList[1]).upper()
        else :
            l_url = url + self.master_data[str(reqList[1]).upper()]['id'] + convert \
               + self.master_data[str(reqList[2]).upper()]["symbol"]
        return l_url

    def convert_coin_to_othercurrency(self, req):
        reqList = req[4:].split(" ")
        resp=''
        try :
            self.validate_data(reqList)
            urlLocal = self.frame_url(reqList)
            self.convert_response = requests.get(urlLocal, data=params).json()
            resp = self.format_convert_response(reqList)
        except CE.DataException as DE:
            raise CE.finalException(DE.errorMessage)
        return resp

    def get_response_from_api(self):
        threading.Timer(300, self.get_response_from_api).start()
        self.response = requests.get(url + convertINR, data=params).json()
        self.prepare_master_data()

    def get_coin_data_from_cache(self, req):
        try:
            ret = self.master_data[req]['response']
        except KeyError:
            ret = req + ' not found' + neutralface
        return ret

    def get_message_to_send(self, req):
        req_list = req[4:].split(",")
        respMessage = ''
        for i in req_list:
            if str(i) == "":
                continue
            respCrypt = self.get_coin_data_from_cache(str(i).strip().upper())
            respMessage = respMessage + ' ' + respCrypt.strip() + '\n'
        return respMessage