from flask import Flask
from multiprocessing import shared_memory

app = Flask(__name__)

try:
    idle_mark = shared_memory.SharedMemory(name='tg_idle', create=True, size=1)
except FileExistsError:
    idle_mark = shared_memory.SharedMemory(name='tg_idle', create=False)


@app.route('/', methods=['GET'])
def online():
    return '@KumaTea_bot is online.', 200


@app.route('/status', methods=['GET'])
def status():
    if idle_mark.buf[0]:
        return 'Idle', 200
    else:
        return 'Busy', 200


if __name__ == '__main__':
    app.run(host='localhost', port=10560, debug=False)
