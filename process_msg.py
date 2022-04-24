from link import link_process


def process_msg(client, message):
    if message and (message.text or message.caption):
        return link_process(message)
    else:
        return None
