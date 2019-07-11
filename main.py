from flask import Flask, request as flaskreq
from msgType import msg_type

app = Flask(__name__)


@app.route('/', methods=['POST'])
def main():
    data = flaskreq.json
    # print(data)
    resp = msg_type(data)
    # logcsv(data, resp)
    return '', 200


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=False)
