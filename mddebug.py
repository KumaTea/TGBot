# import os
import json
from dataio import sendmsg  # sendfile, sendphoto
# import pyscreenshot as scrshot
# from flask import request as flaskreq
# from threading import Timer
from starting import getadminid


def mddebug(data, log=False):
    adminid = getadminid()
    debugmsg = json.dumps(data)
    sendmsg(adminid[0], debugmsg)
    """
    if log:
        sendfile(adminid[0], 'log/log.csv', False, 'upload')
    if os.name == 'nt':
        scrst = scrshot.grab()
        scrst.save('log/screenshot.png')
        sendphoto(adminid, 'log/screenshot.png', False, 'upload')
    """
    return 'DEBUG FINISHED'


"""
def serveroff():
    func = flaskreq.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


def mdexit():
    tm = Timer(5, serveroff)
    tm.start()
"""
