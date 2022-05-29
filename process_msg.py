try:
    from local_functions import local_process
except ImportError:
    def local_process(m):
        return None


def process_msg(client, message):
    if message and (message.text or message.caption):
        return local_process(message)
    else:
        return None
