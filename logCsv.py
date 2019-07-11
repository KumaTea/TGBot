import json
from datetime import datetime


def log_csv(request, response):
    with open('log/log.csv', 'a') as log:
        if 'message' in request:
            username = request['message']['from'].get('username', 'NoUsername')
            # using get('username') instead of ['username']
            # to avoid errors when no username
        elif 'edited_message' in request:
            username = request['edited_message']['from'].get('username', 'NoUsername')
        elif 'channel_post' in request:
            username = request['channel_post']['chat'].get('username', 'NoUsername')
        elif 'edited_channel_post' in request:
            username = request['edited_channel_post']['chat'].get('username', 'NoUsername')
        else:
            username = 'User not found'

        if type(response) == dict:
            resp = json.dumps(response).replace(',', '.')
            # csv
        elif type(response) == str:
            resp = response
        else:
            resp = 'None'
        log.write('{},{},{},{},{}\n'.format(datetime.now().strftime('%Y-%m-%d'), datetime.now().strftime('%H:%M:%S'), username, json.dumps(request).replace(',', '.'), resp))
