from common.info import debug_mode, administrators


if debug_mode:
    pwd = 'D:/GitHub/TGBot'
else:
    pwd = '/home/kuma/bots/TGBot'

restart_mark = f'{pwd}/tmp/tgbot-restart-by.txt'

brackets_re = r'\([\s　]*\)|（[\s　]*）'
title_re = r'《.+》'

nonsense_replies = ('咋会这样呢 对对对 好家伙 说的是啊 谁不是呢 振作点儿 真过意不去 好说好说 简直难以想象 有道理 上班不忙吗 你不上班吗 你很无聊吗 最近很闲吗 我觉得也是 wow 确实 可以的 厉害了 '
                    '我都行，看你 太棒了 蛮好的 不错 别见外 啊？这也太内个了吧 太过分了 咋能这样呢 这叫啥事啊 这人也真是 怎么回事 真有你的 原来是这样 我就知道 还是你厉害，我就不行 '
                    '我可以理解为这是高级凡尔赛吗 怎么能这样呢 哇 嚯 害 服了 详细说说 开眼界了 好问题 会好的 笑死 真的耶 怎么啦 难搞哦 我懂 妈耶 还是要打起精神来 我也这么觉得 就是...（个人理解） '
                    '真的吗！好厉害 啊是吗？ 我也是 那也是 你知道我多想成为你吗 对对对 不愧是你 我觉得挺牛的 可不是嘛 你说的没错 看你自己 也没啥意思 生活嘛 抱抱你，太心疼了 太生气了 好惨啊 '
                    '咋能这样啊 我也生气了 无语了 666 真行啊 都这样 咋欺负人呢 不难过了哦 会好起来的 硬着头皮上吧，慢慢来 为什么？ 怎么会？ 真的啊？ 我都不知道谀！ 那怎么办？ 后来呢？ '
                    '原来是这样！ 我辈楷模 有内味儿了 瑞思拜 大佬大佬 学到了 interesting nice fine good omg 那还挺好的 那就先这样 好像是有点儿 没事儿 美女的事你少管 '
                    '哈哈不用啦 确实，该干嘛就干嘛').split()

greet_message = (
    '/start: 发送这条消息\n'
    '/help: 也是发送这条消息\n'
    '/ping: 检测延迟\n'
    '/rp: 复读\n'
    '\n'
    '本 bot 还有更多功能静待发现：\n'
    '/title /enable_group /mbti 等\n'
    '\n'
    '如果你是 qljj (情侣阶级 / 有恋爱史)，请 [点击此链接](https://t.me/kumatea_bot?start=r_q) 告诉我。\n'
    '如果你是 g/f2d (官 / 富二代)，请 [点击此链接](https://t.me/kumatea_bot?start=r_f) 告诉我。\n'
    '点击后，你可能需要再点击一次下方的 start 按钮。'
)
unknown_message = "I can't understand your message or command. You may try /help."

poll_groups_file = f'{pwd}/data/poll/groups.txt'
poll_candidates_file = f'{pwd}/data/poll/candidates.p'
poll_admins = administrators  # .copy()

kw_reply_dict = {
    'envy': {
        'keywords': ['xm', '羡慕', '好酸'],
        'reply': 'xmsl 😭',
        'quote': False
    },
    'want': {
        'keywords': ['好想'],
        'reply': 'RANDUSER也好想 🥺',
        'quote': False
    },
    'rule': {
        'keywords': ['不行', '不可以', '不能'],
        'reply': 'RANDUSER可以',
        'skip': ['行不行', '可不可以', '可以不可以', '能不能'],
        'quote': False
    },
}

group_help = (
    '/rp: repeat\n'
    '/title: manage titles\n'
    '/ping: check for delay\n'
    '/debug: display debug info\n'
    '\n'
    '可用子帮助：\n'
    'title: `help title`\n'
    'poll: `help poll`'
)

title_help = '用法\n' \
        '向对象的消息 **回复** `/title <text>` 以添加头衔\n' \
        '字数 **16** 以内，不支持 emoji\n\n' \
        '`/title list` 列出所有头衔'

poll_help = (
    '用法\n'
    '/enroll_poll 昵称: 加入抽奖池\n'
    '/leave_poll: 退出抽奖池\n'
    '/view_poll: 查看奖池\n'
    '\n'
    '昵称注意事项\n'
    '1. 必须以「比」「批」结尾或为叠词\n'
    '2. 昵称必须为2字，半角字符记为0.5个字\n'
    '3. 昵称不能重复\n'
    '4. 原则上，g/f2d 及有恋爱史者使用「批」'
)

cue_exact = ['kuma', '库玛']
cue_prob = ['kmt', '蓝毛']

REFUSE_STICKER = 'CAACAgIAAxkBAAIfbGXhYdn67j4-3hpsMSddd24BSltgAAKSOwACo-wIS-Sd1NbsOlHnHgQ'
