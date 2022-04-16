from telegram import Update
from starting import starting
from botSession import kuma, dp, idle_mark
from flask import Flask, request as flask_req


app = Flask(__name__)

starting()


@app.route('/', methods=['GET'])
def online():
    return '@KumaTea_bot is online.', 200


@app.route('/', methods=['POST'])
def main():
    idle_mark.buf[0] = 0
    update = Update.de_json(flask_req.json, kuma)
    dp.process_update(update)
    idle_mark.buf[0] = 1
    return '', 200


@app.route('/status', methods=['GET'])
def status():
    if idle_mark.buf[0]:
        return 'Idle', 200
    else:
        return 'Busy', 200


if __name__ == '__main__':
    app.run(host='localhost', port=10560, debug=False)
