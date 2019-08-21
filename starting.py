import os


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
    apiex = os.path.isfile('token.txt')
    if apiex:
        with open('token.txt', 'r') as api:
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
        adminid = [0]  # not set!
    return adminid


def set_proxy(ip='127.0.0.1', port='1080', protocol='http'):
    proxy = f'{protocol}://{ip}:{port}'
    os.environ['http_proxy'] = proxy
    os.environ['HTTP_PROXY'] = proxy
    os.environ['https_proxy'] = proxy
    os.environ['HTTPS_PROXY'] = proxy
