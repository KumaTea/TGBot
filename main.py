import botDB
from telegram import Update
from botTools import set_busy
from starting import starting
from botSession import kuma, dp
from flask import Flask, request as flask_req


app = Flask(__name__)

starting()


@app.route('/', methods=['GET'])
def online():
    return '@KumaTea_bot is online.', 200


@app.route('/', methods=['POST'])
@set_busy
def main():
    update = Update.de_json(flask_req.json, kuma)
    dp.process_update(update)
    return '', 200


@app.route('/status', methods=['GET'])
def status():
    if botDB.is_idle:
        return 'Idle', 200
    else:
        return 'Busy', 200


if __name__ == '__main__':
    app.run(host='localhost', port=10560, debug=False)
