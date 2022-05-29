from session import idle_mark


def set_busy(operation):
    def wrapper(*args, **kwargs):
        idle_mark.buf[0] = 0
        operation(*args, **kwargs)
        idle_mark.buf[0] = 1
    return wrapper
