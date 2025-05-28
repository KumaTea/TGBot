import asyncio
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


async def forward_and_delete(fw_chat_id: int, del_chat_id: int):
    history_count = await me.get_chat_history_count(del_chat_id)

    # 50 messages at once
    pbar = trange(history_count // 50 + 1)

    for msg_batch_id in pbar:
        pbar.set_description(f'Batch {msg_batch_id}')
        message_ids = list(range(50 * msg_batch_id + 1, min(50 * msg_batch_id + 50 + 1, history_count + 1)))

        try:
            await me.forward_messages(fw_chat_id, del_chat_id, message_ids)
            await asyncio.sleep(1)
            # await me.delete_messages(del_chat_id, message_ids)
            await asyncio.sleep(30)
        except Exception as e:  # some message ids are missing
            input(str(e))
            pbar.write(f'At batch {msg_batch_id} some message ids are missing...')
            for message_id in message_ids:
                try:
                    await me.forward_messages(fw_chat_id, del_chat_id, message_id)
                    await asyncio.sleep(1)
                    # await me.delete_messages(del_chat_id, message_id)
                except Exception as ee:
                    input(str(ee))
                    pass

    # pbar.close()
    print('Forwarded and deleted successfully!')
    return True


if __name__ == '__main__':
    print('Deleting messages')
    c_id = int(input('Chat ID: '))
    u_id = int(input('User ID: ') or creator)
    t = int(input('Total messages to delete: ') or 0)
    with me:
        me.run(main(c_id, u_id, t))
