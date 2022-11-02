import json
from requests import Session
from operator import itemgetter

def getInfo (headers, limit=200):

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'convert': 'EUR',
        'limit':str(limit)
    }
    session = Session()
    session.headers.update(headers)
    response = session.get(url, params=parameters)
    crypto_list_source = json.loads(response.text)['data'] 
    crypto_list = []
    for i in range(len(crypto_list_source)):
        crypto_name = crypto_list_source[i]["name"]
        crypto_price = crypto_list_source[i]['quote']['EUR']['price']
        crypto_change = crypto_list_source[i]['quote']['EUR']['percent_change_24h']
        crypto_list.append([crypto_name, crypto_price, crypto_change])
    crypto_list = sorted(crypto_list, key=itemgetter(2))
    return crypto_list
