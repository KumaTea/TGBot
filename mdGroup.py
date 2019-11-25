from mdGroupCmd import group_cmd
from mdNewMember import welcome
from botSession import bot
from botInfo import self_id


class Group:

    def __init__(self, data):
        self.data = data
        bot_getter = bot.get(data)
        self.chat_id = bot_getter.chat('id')
        self.msg_id = bot_getter.message('id')
        self.is_reply = bot_getter.reply('id')

    def new_member(self, data=None):
        if not data:
            data = self.data
        if not data['message']['new_chat_member']['is_bot']:
            resp = welcome(self.chat_id, data['message']['new_chat_member']['id'], self.msg_id)
            return resp
        else:
            return 'Is bot'

    def text(self, data=None):
        if not data:
            data = self.data
        msg = bot.get(data).message()
        resp = False
        if msg.startswith('/'):
            resp = group_cmd(data)
        return resp

    def sticker(self, data=None):
        if not data:
            data = self.data
        resp = False
        if self.is_reply == self_id:
            sticker = bot.get(data).sticker()
            resp = bot.send(self.chat_id).sticker(sticker, reply_to=self.msg_id)
        return resp

    def photo(self, data=None):
        if not data:
            data = self.data
        resp = False
        if self.is_reply == self_id:
            photo = bot.get(data).photo()
            resp = bot.send(self.chat_id).photo(photo, reply_to=self.msg_id)
        return resp

    def video(self, data=None):
        if not data:
            data = self.data
        resp = False
        if self.is_reply == self_id:
            video = bot.get(data).video()
            resp = bot.send(self.chat_id).video(video, reply_to=self.msg_id)
        return resp

    def file(self, data=None):
        if not data:
            data = self.data
        resp = False
        if self.is_reply == self_id:
            file = bot.get(data).document()
            resp = bot.send(self.chat_id).file(file, reply_to=self.msg_id)
        return resp

    def gif(self, data=None):
        if not data:
            data = self.data
        resp = False
        if self.is_reply == self_id:
            file = bot.get(data).gif()
            resp = bot.send(self.chat_id).gif(file, reply_to=self.msg_id)
        return resp
