from dataio import getchatid, sendmsg, sendsticker


def newmem(data):
    if not data['message']['new_chat_member']['is_bot']:
        groupid = getchatid(data)
        sendmsg(groupid, '欢迎新大佬！')
        resp = sendsticker(groupid, 'CAADBQADgAADMwMcCJWbCk051Y0BAg')
        return resp
