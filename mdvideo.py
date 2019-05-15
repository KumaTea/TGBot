from dataio import getchatid, sendmsg


def mdvideo(data):
    chatid = getchatid(data)
    rectext = 'I have received your video. But I can\'t deal with it now! Please wait for future updates.'
    resp = sendmsg(chatid, rectext)
    return resp
