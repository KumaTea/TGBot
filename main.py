from bot.session import kuma

if not debug_mode:
    import uvloop
    uvloop.install()


from bot.starting import starting
from common.data import debug_mode


starting()


if __name__ == '__main__':
    kuma.run()
