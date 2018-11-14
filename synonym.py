import requests
import json
import random
import time
import keys

random.seed(time.gmtime())
class OxfordBotHandler:
    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key
        self.url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/en/'
        self.config = {'app_id': app_id, 'app_key': app_key}
    def getSynonyms(self, word):
        r = requests.get(self.url+word.lower()+'/synonyms', headers = self.config)
        if r.status_code != 200:
            return 'Not available...'
        senses = r.json()['results'][0]['lexicalEntries'][0]['entries'][0]['senses']
        randId = random.randint(0, len(senses)-1)
        random.shuffle(senses[randId]['synonyms'])
        r = min(len(senses[randId]['synonyms']), 6)
        syn_list = ""
        for text in range(0, r):
            syn_list += '`'+senses[randId]['synonyms'][text]['text']+"`\n"
        return syn_list
dict408 = OxfordBotHandler(keys.app_id(), keys.app_key())
def getSynonyms(word):
    return dict408.getSynonyms(word)