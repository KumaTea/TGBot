import sys
import info
import random
from session import kuma
from tools import get_file
from bot_db import restart_mark


def private_start(client, message):
    return message.reply(info.start_message)


def private_help(client, message):
    help_msg = f'{info.help_message}\n\nI\'m in my {info.version} ({info.channel}) version.'
    return message.reply(help_msg)


def private_forward(client, message):
    command = message.text
    content_index = command.find(' ')
    user = message.from_user
    if content_index == -1:
        resp = message.reply('You haven\'t type in your message!')
    else:
        first = user.first_name
        last = (' ' + user.last_name) if user.last_name else ''
        user_id = user.id
        username = ' (' + (('@' + user.username + ', ') if user.username else '') + str(user_id) + ')'
        forward_msg = first + last + username + '\n\n' + command[content_index+1:]

        kuma.send_message(info.creator, forward_msg)
        resp = message.reply('Message successfully sent.')
    return resp


def fuyan():
    replies = '咋会这样呢 对对对 好家伙 说的是啊 谁不是呢 振作点儿 真过意不去 好说好说 简直难以想象 有道理 上班不忙吗 你不上班吗 你很无聊吗 最近很闲吗 我觉得也是 wow 确实 可以的 厉害了 我都行，看你 太棒了 蛮好的 不错 别见外 啊？这也太内个了吧 太过分了 咋能这样呢 这叫啥事啊 这人也真是 怎么回事 真有你的 原来是这样 我就知道 还是你厉害，我就不行 我可以理解为这是高级凡尔赛吗 怎么能这样呢 哇 嚯 害 服了 详细说说 开眼界了 好问题 会好的 笑死 真的耶 怎么啦 难搞哦 我懂 妈耶 还是要打起精神来 我也这么觉得 就是..（个人理解） 真的吗！好厉害 啊是吗？ 我也是 那也是 你知道我多想成为你吗 对对对 不愧是你 我觉得挺牛的 可不是嘛 你说的没错 看你自己 也没啥意思 生活嘛 抱抱你，太心疼了 太生气了 好惨啊 咋能这样啊 我也生气了 无语了 666 真行啊 都这样 咋欺负人呢 不难过了哦 会好起来的 硬着头皮上吧，慢慢来 为什么？ 怎么会？ 真的啊？ 我都不知道谀！ 那怎么办？ 后来呢？ 原来是这样！ 我辈楷模 有内味儿了 瑞思拜 大佬大佬 学到了 interesting nice fine good omg 那还挺好的 那就先这样 好像是有点儿 没事儿 美女的事你少管 哈哈不用啦 确实，该干嘛就干嘛'
    return random.choice(replies.split())


def private_get_file_id(client, message):
    if message.from_user.id == info.self_id:
        return None
    file_id, file_type = get_file(message)
    if file_type == 'text':
        return message.reply(fuyan())
    if file_id:
        return message.reply(file_id)
    else:
        return message.reply('Unknown type of media.')


def private_unknown(client, message):
    return message.reply("I can't understand your message or command. You may try /help.")


def restart(client, message):
    if message.from_user.id in info.administrators:
        # Do not use subprocess.run since we can't wait for it to finish
        # subprocess.Popen('sleep 2; docker stop tgbot; sleep 2; docker start tgbot', shell=True)
        with open(restart_mark, 'w') as f:
            f.write(str(message.from_user.id))
        message.reply('Restarting...')
        return sys.exit(0)
    else:
        return None  # 无事发生
