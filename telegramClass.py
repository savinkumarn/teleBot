import requests
import cryptoClass
import customExceptions as CE

url = "https://api.telegram.org/bot556048452:AAFTauwIsB2USv8mC1skMkFhkaJv4M5yoVc/"
cryp = cryptoClass.cryptoClass()
hand_horns = u'\U0001F918'

def help_menu(junk):
    resp = 'Welcome to HELP Menu\n\n' \
           'use /cp to get coin stats\n' \
           'ex /cp BTC,eth,Sub\n\n' \
           'use /cv to use currency conversion\n' \
           '/cv [amount] [currency] [currency]\n' \
           'ex /cv 3 eth usd\n' \
           'ex /cv 5 btc VEN\n\n' \
           'Enjoy Bitches!!!' + hand_horns + \
           '\n\n PM @savin54'
    return resp

master_func = {
    "/cp": cryp.get_message_to_send,
    "/cv": cryp.convert_coin_to_othercurrency,
    "/hp": help_menu
}

class telegramClass():
    """
    This class is used to create a Telegram class
    """
    def __init__(self):
        """
        Constructor
        """
        self.update_id=0

    def get_updates_json(self, request):
        params = {'timeout': 100, 'offset': None}
        response = requests.get(request + 'getUpdates', data=params)
        return response.json()

    def last_update(self, data):
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
                    resp_message = master_func[update['message']['text'][:3]](update['message']['text'])
                except CE.finalException as FE:
                    resp_message = FE.errorMessage
                except KeyError:
                    resp_message = "Use /hp for help"
                self.send_mess(resp_message)
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

