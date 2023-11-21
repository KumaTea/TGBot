from common.data import debug_mode

if not debug_mode:
    import uvloop
    uvloop.install()

from bot.session import kuma
from bot.starting import starting


starting()


if __name__ == '__main__':
    kuma.run()
