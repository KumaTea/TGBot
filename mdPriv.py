from mdPrivCmd import priv_cmd
from botSession import bot


class Private:
    
    def __init__(self, data):
        self.data = data
        self.chat_id = bot.get(data).chat('id')

    def text(self, data=None):
        if not data:
            data = self.data
        msg = bot.get(data).message('text')
        if msg.startswith('/'):
            resp = priv_cmd(data)
        else:
            resp = bot.send(self.chat_id).message(msg)
        return resp

    def sticker(self, data=None):
        if not data:
            data = self.data
        sticker = bot.get(data).file()
        resp = bot.send(self.chat_id).message(sticker)
        return resp

    def photo(self, data=None):
        if not data:
            data = self.data
        photo = bot.get(data).file()
        resp = bot.send(self.chat_id).message(photo)
        return resp

    def video(self, data=None):
        if not data:
            data = self.data
        video = bot.get(data).file()
        resp = bot.send(self.chat_id).message(video)
        return resp

    def file(self, data=None):
        if not data:
            data = self.data
        file = bot.get(data).file()
        resp = bot.send(self.chat_id).message(file)
        return resp

    def gif(self, data=None):
        if not data:
            data = self.data
        file = bot.get(data).file()
        resp = bot.send(self.chat_id).message(file)
        return resp
