from flask import Flask, request as flask_req
from botSession import kuma, dp
from telegram import Update
from register import register_handlers


app = Flask(__name__)

register_handlers()


@app.route('/', methods=['POST'])
def main():
    update = Update.de_json(flask_req.json, kuma)
    dp.process_update(update)
    return '', 200


# If run on local machine:
if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=False)
