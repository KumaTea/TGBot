import time
import asyncio
from pyrogram import Client
# from datetime import datetime


bot = Client(
    'kuma',
    api_id=input('api_id: '),
    api_hash=input('api_hash: '),
    bot_token=input('bot_token: '),
    proxy={
        "scheme": "socks5",  # "socks4", "socks5" and "http" are supported
        "hostname": "10.3.0.99",
        "port": 7891,
        # "username": "username",
        # "password": "password"
    }
)


chat_id = 5273618487
msg_id = 8395

groups = 5
trails = 10


async def check_once(group: int = 0, trial: int = 0) -> float:
    # test_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # sync client
    await bot.get_messages(chat_id, msg_id)

    start_time = time.perf_counter()
    # message = await bot.edit_message_text(chat_id, msg_id, test_string)
    await bot.get_messages(chat_id, msg_id)
    end_time = time.perf_counter()

    latency = 1000*(end_time - start_time)
    print(f'Group: {group:>2}, Trial: {trial:>2}, Latency: {latency:.2f}ms')
    return latency


def print_results(latency_pairs: list[tuple[float, float, float]]):
    for group in range(groups):
        min_latency, max_latency, avg_latency = latency_pairs[group]
        print(f'Group {group:>2}: Min {min_latency:.2f}ms, Max {max_latency:.2f}ms, Avg {avg_latency:.2f}ms')


async def check_latency():
    print('Starting latency check...')
    # init
    await bot.get_me()

    latency_pairs: list[tuple[float, float, float]] = []  # min, max, avg
    for group in range(groups):
        latencies: list[float] = []
        for trial in range(trails):
            latency = await check_once(group, trial)
            latencies.append(latency)
            await asyncio.sleep(2)

        assert len(latencies) == trails, f'Group {group} has {len(latencies)} latencies, expected {trails}.'
        # remove min and max
        latencies.sort()
        latencies = latencies[1:-1]
        min_latency = latencies[0]
        max_latency = latencies[-1]
        avg_latency = sum(latencies) / len(latencies)
        latency_pairs.append((min_latency, max_latency, avg_latency))

    print_results(latency_pairs)


if __name__ == '__main__':
    bot.start()
    # bot.run(check_latency())
    # pyrogram has a `bot.run(coroutine)` method
    # but `kurigram` (this fork) removes it
    # while `pyrofork`, `hydrogram` and others remains
    # loop = asyncio.get_event_loop()
    loop = bot.loop
    loop.run_until_complete(check_latency())
    print('Latency check completed.')
    bot.stop()
    # loop.close()
