from tqdm import trange
from pyrogram import Client
from bot.session import config
from common.info import creator
from pyrogram.errors.exceptions.forbidden_403 import ChatAdminRequired


me = Client(
    'me',
    api_id=config['kuma']['api_id'],
    api_hash=config['kuma']['api_hash']
)


async def main(chat_id: int, user_id: int = creator, total: int = 0):
    # first try if is admin
    try:
        result = await me.delete_user_history(chat_id=chat_id, user_id=user_id)
        if result:
            print('Deleted successfully!')
            return True
    except ChatAdminRequired:
        print('Not admin, fallback to delete messages one by one')

    # delete messages one by one
    assert user_id == creator  # can only delete own messages

    total = total or 9999
    pbar = trange(total)

    async for message in me.get_chat_history(chat_id):
        if message.from_user and message.from_user.id == user_id:
            await me.delete_messages(chat_id, message.id)
            pbar.set_description(f'Deleted: {message.id}\t' + str(message.text).replace('\n', ' ')[:50])
            pbar.update(1)
            if pbar.n >= total:
                break

    pbar.close()
    print('Deleted successfully!')
    return True


if __name__ == '__main__':
    print('Deleting messages')
    c_id = int(input('Chat ID: '))
    u_id = int(input('User ID: ') or creator)
    t = int(input('Total messages to delete: ') or 0)
    with me:
        me.run(main(c_id, u_id, t))

