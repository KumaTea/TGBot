from dataio import getchatid, sendmsg


def dealdoc(data):
    chatid = getchatid(data)
    rectext = 'I have received your document. But I can\'t deal with it now! Please wait for future updates.'
    resp = sendmsg(chatid, rectext)
    return resp
