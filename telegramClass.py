import requests
import cryptoClass

url = "https://api.telegram.org/bot556048452:AAFTauwIsB2USv8mC1skMkFhkaJv4M5yoVc/"


class telegramClass():
    '''
    This class is used to create a report class
    '''
    def __init__(self):
        '''
        Constructor
        '''
        update_id=0

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

    def send_mess(self, chat, text):
        params = {'chat_id': chat, 'text': text}
        response = requests.post(url + 'sendMessage', data=params)
        return response

    def get_message_to_send(self, req, cryp):
        req_list = req.split(",")
        respMessage = ''
        for i in req_list:
            if str(i) == "":
                continue
            respCrypt = cryp.get_coin_data_from_api(str(i).strip().upper())
            respMessage = respMessage + ' ' + respCrypt.strip() + '\n'
        return respMessage


    def get_coin_data(self):
        cryp = cryptoClass.cryptoClass("", {})
        cryp.get_response_from_api()
        while True:
            update = self.last_update(self.get_updates_json(url))
            if self.update_id == update['update_id']:
                if update['message']['text'][:3] == "/lc":
                    respMessage=self.get_message_to_send(update['message']['text'][4:], cryp)
                    self.send_mess(self.get_chat_id(), respMessage)
                self.update_id += 1


    def check_updates(self):

        while True:
            if self.get_updates_json(url) is not None:
                self.update_id = self.last_update(self.get_updates_json(url))['update_id']
                break

        self.get_coin_data()

