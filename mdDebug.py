import json
from dataIO import send_msg
from starting import getadminid


def md_debug(data, log=False):
    admin_id = getadminid()
    debug_msg = json.dumps(data)
    send_msg(admin_id[0], debug_msg)
    """
    if log:
        sendfile(admin_id[0], 'log/log.csv', False, 'upload')
    if os.name == 'nt':
        scrst = scrshot.grab()
        scrst.save('log/screenshot.png')
        sendphoto(admin_id, 'log/screenshot.png', False, 'upload')
    """
    return 'DEBUG FINISHED'
