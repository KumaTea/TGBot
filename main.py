from flask import Flask, request as flask_req
from msgType import msg_type
# from starting import set_proxy

app = Flask(__name__)
# set_proxy()


@app.route('/', methods=['POST'])
def main():
    data = flask_req.json
    # print(data)
    resp = msg_type(data)
    # print(f'\n\n{resp}\n\n')
    return '', 200


if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=False)
