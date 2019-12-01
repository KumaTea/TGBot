from flask import Flask, request as flask_req
from msgType import msg_type
import logging


app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.route('/', methods=['POST'])
def main():
    data = flask_req.json
    msg_type(data)
    return '', 200


# If run on local machine:
if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=False)
