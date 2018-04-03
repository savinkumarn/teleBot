from locale import currency

import requests
import threading
import customExceptions as CE

smileface = u'\U0001F601'
sadface = u'\U0001F641'
neutralface = u'\U0001F928'
first_element = 0
second_element = 1
third_element = 2

url = "https://api.coinmarketcap.com/v1/ticker/"
convertINR = "/?convert=INR&limit=200"
convert = "/?convert="
params = {'timeout': 100, 'offset': None}
currency_list = ["AUD", "BRL", "CAD", "CHF", "CLP", "CNY", "CZK",
               "DKK", "EUR", "GBP", "HKD", "HUF", "IDR", "ILS", "INR", "JPY",
               "KRW", "MXN", "MYR", "NOK", "NZD", "PHP", "PKR", "PLN", "RUB", "SEK",
               "SGD", "THB", "TRY", "TWD", "ZAR", "USD"]

class cryptoClass():
    """
    This class is used to create a Crupto class
    """
    def __init__(self):
        """
        Class Initialization
        """
        self.response = ''
        self.master_data = {}
        self.convert_response = ''

    def validate_data(self, inputList):
        if len(inputList) < 3:
            raise CE.DataException('Not enough arguments , use /hp for help')
        elif len(inputList) > 3:
            raise CE.DataException('What are you trying to do ?, use /hp for help')
        else :
            try:
                float(inputList[first_element])
                self.master_data[str(inputList[second_element]).upper()]
                self.master_data[str(inputList[third_element]).upper()]
            except ValueError:
                raise CE.DataException('I take numbers as first argument, use /hp for help')
            except KeyError:
                if str(inputList[1]).upper() in currency_list or str(inputList[2]).upper() in currency_list:
                    return
                else :
                    raise CE.DataException('Conversion not possible ,use /hp for help')

    def prepare_master_data(self):
        for i in self.response:
            resp = i['symbol'] + ' $' + str('{:.2f}'.format(float(i['price_usd']))) + ' INR' + \
                   str('{:.2f}'.format(float(i['price_inr']))) + ' ' + i['percent_change_1h'] \
                   + '% ' + (smileface if float(i['percent_change_1h']) > 0 else sadface)
            inner_dict = {
                'id': i['id'],
                'response': resp
            }
            self.master_data[i['symbol'].upper()] = inner_dict

    def format_convert_response(self, reqList):
        if str(reqList[second_element]).upper() in currency_list:
            priceVar = 'price_' + str(reqList[second_element]).lower()
            totalConv = float(reqList[first_element]) / float(self.convert_response[first_element][priceVar])
        else:
            priceVar = 'price_' + str(reqList[third_element]).lower()
            totalConv = float(self.convert_response[first_element][priceVar]) * float(reqList[first_element])

        return reqList[first_element] + ' ' + str(reqList[second_element]).upper() + ' = ' \
               + str('{:.5f}'.format(totalConv)) + ' ' + str(reqList[third_element]).upper()

    def frame_url(self, reqList):
        if str(reqList[third_element]).upper() in currency_list:
            l_url = url + self.master_data[str(reqList[second_element]).upper()]['id'] + convert \
                    + str(reqList[2]).upper()
        elif str(reqList[second_element]).upper() in currency_list:
            l_url = url + self.master_data[str(reqList[third_element]).upper()]['id'] + convert \
                    + str(reqList[1]).upper()
        else:
            l_url = url + self.master_data[str(reqList[second_element]).upper()]['id'] + convert \
               + self.master_data[str(reqList[third_element]).upper()]["symbol"]
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