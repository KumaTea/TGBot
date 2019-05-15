from dataio import getchatid
from mdcmdgrp import mdcmdgrp
from mdcmdpriv import mdcmdpriv


def mdcmd(data):
    chatid = getchatid(data)

    if chatid < 0:
        resp = mdcmdgrp(data)
        return resp
    else:
        resp = mdcmdpriv(data)
        return resp
