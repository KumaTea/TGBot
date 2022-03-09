from mdLink import link_process


def process_msg(update, context):
    message = update.message
    # try:
    #     chat_id = message.chat_id
    # except AttributeError:
    #     return None  # edited message
    # message_id = message.message_id

    if message and (message.text or message.caption):
        return link_process(message)
    else:
        # print(message)
        return None
