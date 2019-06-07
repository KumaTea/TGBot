import json
from datetime import datetime


def logcsv(request, response):
    with open('log/log.csv', 'a') as log:
        if 'message' in request:
            usrnm = request['message']['from'].get('username', 'NoUsername')
            # using get('username') instead of ['username']
            # to avoid errors when no username
        elif 'edited_message' in request:
            usrnm = request['edited_message']['from'].get('username', 'NoUsername')
        elif 'channel_post' in request:
            usrnm = request['channel_post']['chat'].get('username', 'NoUsername')
        elif 'edited_channel_post' in request:
            usrnm = request['edited_channel_post']['chat'].get('username', 'NoUsername')
        else:
            usrnm = 'User not found'

        if type(response) == dict:
            resp = json.dumps(response).replace(',', '.')
            # csv
        elif type(response) == str:
            resp = response
        else:
            resp = 'None'
        log.write('{},{},{},{},{}\n'.format(datetime.now().strftime('%Y-%m-%d'), datetime.now().strftime('%H:%M:%S'), usrnm, json.dumps(request).replace(',', '.'), resp))
