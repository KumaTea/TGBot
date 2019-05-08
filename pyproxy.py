import os


def setproxy():
    lcproxy = 'http://127.0.0.1:10080'
    os.environ['http_proxy'] = lcproxy
    os.environ['HTTP_PROXY'] = lcproxy
    os.environ['https_proxy'] = lcproxy
    os.environ['HTTPS_PROXY'] = lcproxy
