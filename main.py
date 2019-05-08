from bottle import run, post, request as bottlereq
from pyproxy import setproxy
from dataio import setapi
from msgtype import dealtype
from starting import starting
from logcsv import logcsv

setproxy()
setapi()


@post('/')
def main():
    data = bottlereq.json
    # print(data)
    resp = dealtype(data)
    logcsv(data, resp)


starting()
if __name__ == '__main__':
    run(host='localhost', port=10568, debug=True)
