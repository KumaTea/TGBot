from telegram import Update
from starting import starting
from botSession import kuma, dp
from flask import Flask, request as flask_req


app = Flask(__name__)

starting()


@app.route('/', methods=['GET'])
def status():
    return '@KumaTea_bot is online.', 200


@app.route('/', methods=['POST'])
def main():
    update = Update.de_json(flask_req.json, kuma)
    dp.process_update(update)
    return '', 200


# If run on local machine:
if __name__ == '__main__':
    app.run(host='localhost', port=10560, debug=False)
