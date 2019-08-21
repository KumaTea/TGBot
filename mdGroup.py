from mdGroupCmd import group_cmd
from botDb import welcome_msg
from botSession import bot


class Group:

    def __init__(self, data):
        self.data = data
        self.chat_id = bot.get(data).chat('id')
        self.msg_id = bot.get(data).message('id')

    def new_member(self, data=None):
        if not data:
            data = self.data
        if not data['message']['new_chat_member']['is_bot']:
            if welcome_msg.get(self.chat_id) is not None:
                resp = 'Initialize'
                if welcome_msg[self.chat_id].get('message') is not None:
                    resp = bot.send(self.chat_id).message(welcome_msg[self.chat_id]['message'])
                if welcome_msg[self.chat_id].get('sticker') is not None:
                    resp = bot.send(self.chat_id).sticker(welcome_msg[self.chat_id]['message'])
            else:
                resp = 'Not familiar using default'
            return resp
        else:
            return 'Is bot'

    def text(self, data=None):
        if not data:
            data = self.data
        msg = bot.get(data).message()
        if msg.startswith('/'):
            resp = group_cmd(data)
        else:
            resp = bot.send(self.chat_id).message(msg, reply_to=self.msg_id)
        return resp

    def sticker(self, data=None):
        if not data:
            data = self.data
        sticker = bot.get(data).sticker()
        resp = bot.send(self.chat_id).sticker(sticker, reply_to=self.msg_id)
        return resp

    def photo(self, data=None):
        if not data:
            data = self.data
        photo = bot.get(data).photo()
        resp = bot.send(self.chat_id).photo(photo, reply_to=self.msg_id)
        return resp

    def video(self, data=None):
        if not data:
            data = self.data
        video = bot.get(data).video()
        resp = bot.send(self.chat_id).video(video, reply_to=self.msg_id)
        return resp

    def file(self, data=None):
        if not data:
            data = self.data
        file = bot.get(data).document()
        resp = bot.send(self.chat_id).file(file, reply_to=self.msg_id)
        return resp

    def gif(self, data=None):
        if not data:
            data = self.data
        file = bot.get(data).gif()
        resp = bot.send(self.chat_id).gif(file, reply_to=self.msg_id)
        return resp
