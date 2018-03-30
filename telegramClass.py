import requests
import cryptoClass
import customExceptions as CE

url = "https://api.telegram.org/bot556048452:AAFTauwIsB2USv8mC1skMkFhkaJv4M5yoVc/"
cryp = cryptoClass.cryptoClass()
hand_horns = u'\U0001F918'

def help_menu(junk):
    resp = 'Welcome to help menu\n' \
           'use /lc to get coin stats\n' \
           'ex /lc BTC,eth,Sub\n' \
           'use /cv to use conversion\n' \
           'ex /cv 4 btc eth\n' \
           'ex /cv 3 eth usd\n' \
           'Enjoy Bitches!!!'+hand_horns
    return resp

master_func = {
    "/lc": cryp.get_message_to_send,
    "/cv": cryp.convert_coin_to_othercurrency,
    "/hp": help_menu
}

class telegramClass():
    '''
    This class is used to create a report class
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.update_id=0

    def get_updates_json(self,request):
        params = {'timeout': 100, 'offset': None}
        response = requests.get(request + 'getUpdates', data=params)
        return response.json()

    def last_update(self,data):
        results = data['result']
        total_updates = len(results) - 1
        return results[total_updates]

    def get_chat_id(self):
        update=self.last_update(self.get_updates_json(url))
        chat_id = update['message']['chat']['id']
        return chat_id

    def send_mess(self, text):
        params = {'chat_id': self.get_chat_id(), 'text': text}
        response = requests.post(url + 'sendMessage', data=params)
        return response

    def get_data(self):

        while True:
            update = self.last_update(self.get_updates_json(url))
            if self.update_id == update['update_id']:
                try:
                    respMessage = master_func[update['message']['text'][:3]](update['message']['text'])
                except CE.finalException as FE:
                    respMessage= FE.errorMessage
                except KeyError:
                    respMessage = "Use /hp for help you stupid fuck"
                self.send_mess(respMessage)
                self.update_id += 1

    def initialize_app(self):
        while True:
            if self.get_updates_json(url) is not None:
                self.update_id = self.last_update(self.get_updates_json(url))['update_id']
                break
        cryp.get_response_from_api()

    def check_updates(self):
        self.initialize_app()
        self.get_data()

