from link import link_process
try:
    from local_functions import replace_brackets
except ImportError:
    def replace_brackets(m):
        return None


def process_msg(client, message):
    if message and (message.text or message.caption):
        return link_process(message) or replace_brackets(message)
    else:
        return None
