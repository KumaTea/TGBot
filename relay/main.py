# Receive image from Flask and edit message in Telegram

from flask import Flask, request, Response
from telegram import Bot


app = Flask(__name__)
kuma = Bot(token='TOKEN')


@app.route('/api', methods=['POST'])
def main():
    chat_id = request.form['chat_id'] or None
    message_id = request.form['message_id'] or None
    error_msg = request.form['error_msg'] or 'Error!'
    parse_mode = request.form['parse_mode'] or 'Markdown'
    image = request.files['photo'] or None
    if chat_id and message_id and image:
        try:
            edited_media = kuma.edit_message_media(
                chat_id,
                message_id,
                media=image
            )
            kuma.edit_message_caption(
                chat_id, message_id, caption=error_msg, parse_mode=parse_mode)
            return edited_media.photo[-1].file_id
        except Exception as e:
            return str(e), 500
    else:
        return 'Missing parameters', 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10651)
