from session import kuma
from pyrogram.types import InputMediaPhoto


if __name__ == '__main__':
    kuma.send_photo(345060487, input('Type in path: '))

