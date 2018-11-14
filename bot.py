import requests
import datetime
import sys
import keys
from synonym import getSynonyms

class BotHandler:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)
    def get_updates(self, offset=None, timeout=10):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()
        return result_json

    def send_message(self, chat_id, msg, reply):
        params = {'chat_id': chat_id, 'text': msg, 'parse_mode': 'Markdown', 'reply_to_message_id': reply}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()
        if len(get_result['result']) > 0 and ('message' in get_result['result'][-1]):
            return [1, get_result['result'][-1]]
        else:
            return [0]

dict408 = BotHandler(keys.telegramKey())
def query(last):
    last_id = last['update_id']
    last_msg = last['message']
    msg_id = last_msg['message_id']
    chat_id = last_msg['chat']['id']
    if 'text' in last_msg:
        print(last_msg['text'])
        print(dict408.send_message(chat_id, getSynonyms(last_msg['text']), msg_id))
    return last_id + 1

def main():
    new_offset = None
    print('Starting...')
    while True:
        dict408.get_updates(new_offset)
        last = dict408.get_last_update()
        if last[0] == 1:
            new_offset = query(last[1])

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()