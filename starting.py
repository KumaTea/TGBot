import os


def starting():
    if not os.path.exists('log'):
        os.mkdir('log')
    else:
        if os.path.isfile('log/log.old.csv'):
            os.remove('log/log.old.csv')
        if os.path.isfile('log/log.csv'):
            os.rename('log/log.csv', 'log/log.old.csv')

    with open('log/log.csv', 'a') as log:
        log.write('{},{},{},{},{}\n'.format('date', 'time', 'from', 'request', 'response'))

    print('Staring fine.')
