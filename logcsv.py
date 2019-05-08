import json
from datetime import datetime


def logcsv(request, response):
    with open('log/log.csv', 'a') as log:
        if request.get('message') is not None:
            usrnm = request['message']['from'].get('username')
        elif request.get('channel_post') is not None:
            usrnm = request['channel_post']['chat'].get('username')
        elif request.get('edited_channel_post') is not None:
            usrnm = request['edited_channel_post']['chat'].get('username')

        if type(response) == dict:
            resp = json.dumps(response).replace(',', '.')
        elif type(response) == str:
            resp = response
        else:
            resp = 'None'
        log.write('{},{},{},{},{}\n'.format(datetime.now().strftime('%Y-%m-%d'), datetime.now().strftime('%H:%M:%S'), usrnm, json.dumps(request).replace(',', '.'), resp))
