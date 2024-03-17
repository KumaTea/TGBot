from pyrogram import Client
from share.auth import ensure_auth
from func.general import cb_bl_view
from pyrogram.types import CallbackQuery
from mods.poll import poll_callback_handler


@ensure_auth
async def process_callback(client: Client, callback_query: CallbackQuery):
    task = callback_query.data.split('_')[0]
    if task == 'poll':
        return await poll_callback_handler(client, callback_query)
    elif task == 'bl':
        operation = callback_query.data.split('_')[1]
        if operation == 'view':
            return await cb_bl_view(client, callback_query)
    return await callback_query.answer('未知任务', show_alert=True)
