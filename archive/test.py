import asyncio
from session import kuma
from pyrogram.types import InputMediaPhoto


async def main():
    await kuma.send_photo(345060487, InputMediaPhoto(input('Type in path: ')))
    # with open(input('Type in path: '), 'rb') as f:
    #     await kuma.send_photo(345060487, f)


if __name__ == '__main__':
    # kuma.send_photo(345060487, InputMediaPhoto(input('Type in path: ')))
    asyncio.run(main())
