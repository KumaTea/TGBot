from dataio import getchatid, sendmsg


def mdphoto(data):
    chatid = getchatid(data)
    rectext = 'I have received your photo. But I can\'t deal with it now! Please wait for future updates.'
    resp = sendmsg(chatid, rectext)
    return resp
