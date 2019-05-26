import os
from pyproxy import setproxy


def startlog():
    if not os.path.exists('log'):
        os.mkdir('log')
    else:
        if os.path.isfile('log/log.old.csv'):
            os.remove('log/log.old.csv')
        if os.path.isfile('log/log.csv'):
            os.rename('log/log.csv', 'log/log.old.csv')

    with open('log/log.csv', 'a') as log:
        log.write('{},{},{},{},{}\n'.format('date', 'time', 'from', 'request', 'response'))


def setapi():
    botapi = 'https://api.telegram.org/' + input(
        'Please input your bot API.\nIt should start with \"bot\", include \":\" and without \"/\".\n') + '/'
    return botapi


def getapi():
    apiex = os.path.isfile('botapi.txt')
    if apiex:
        with open('botapi.txt', 'r') as api:
            botapi = 'https://api.telegram.org/' + api.read() + '/'
    else:
        botapi = setapi()
    return botapi


def getadminid():
    adminex = os.path.isfile('adminid.txt')
    if adminex:
        with open('adminid.txt', 'r') as admid:
            adminid = list(map(int, admid.readlines()))
    else:
        adminid = [100000000]  # not set!
    return adminid


def starting():
    startlog()
    setproxy()
    print('Starting fine.')
