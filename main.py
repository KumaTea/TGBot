import os

if os.name == 'posix':
    import uvloop
    uvloop.install()


from bot.session import kuma
from bot.starting import starting


starting()


if __name__ == '__main__':
    kuma.run()
