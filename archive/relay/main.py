# Receive image from Flask and edit message in Telegram

import json
import base64
import logging
from io import BytesIO
from telegram import Bot
from telegram import InputMediaPhoto
from flask import Flask, request, Response


def read_file(filename, encrypt=False):
    if encrypt:
        with open(filename, 'rb') as f:
            return base64.b64decode(f.read()).decode('utf-8')
    else:
        with open(filename, 'r') as f:
            return f.read()


def query_token(token_id):
    return read_file(f'token_{token_id}', True)


app = Flask(__name__)
# app.config['DEBUG'] = True
kuma = Bot(query_token(781791363))
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


@app.route('/api', methods=['POST'])
def main():
    # logging.warning('Get new request!')
    # logging.warning(request.form)
    chat_id = request.form['chat_id'] or None
    message_id = request.form['message_id'] or None
    error_msg = request.form['error_msg'] or 'Error!'
    parse_mode = request.form['parse_mode'] or 'Markdown'
    caption = request.form['caption'] or ''
    image = request.files['photo'].read() or None
    if chat_id and message_id and image:
        # logging.info('Sending...')
        try:
            # logging.info('edit_message_media')
            edited_media = kuma.edit_message_media(
                chat_id,
                message_id,
                media=InputMediaPhoto(BytesIO(image))
            )
            if caption:
                caption = caption.replace('**', '*')
                kuma.edit_message_caption(
                    chat_id, message_id, caption=caption, parse_mode=parse_mode)
            logging.info(edited_media.photo[-1].file_id)
            return edited_media.photo[-1].file_id, 200
        except Exception as e:
            if 'time' not in str(e).lower():
                kuma.edit_message_caption(
                    chat_id, message_id, caption=error_msg, parse_mode=parse_mode)
                logging.error(str(e))
                return str(e), 500
            else:
                return '', 200
    else:
        return 'Missing parameters', 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10561)  # , debug=True)
