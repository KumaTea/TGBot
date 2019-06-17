import random
import re
import botdb


def randomjoke(nojo=False):
    jkfl = random.choice(range(7))
    with open('joke/soviet' + str(jkfl), 'r', encoding='utf-8') as joke:
        jk = random.choice(list(joke)).replace('br', '\n')
        if nojo:
            nojoke = re.compile('[^0-9\\n，。、？！（…“”：；‘’《》）]|_')
            jk = re.sub(nojoke, '　', jk)
        return jk


def sysujoke(nojo=False):
    with open('joke/sysu0', 'r', encoding='utf-8') as joke:
        jk = random.choice(list(joke)).replace('br', '\n')
        if nojo:
            nojoke = re.compile('[^0-9\\n，。、？！（…“”：；‘’《》）]|_')
            jk = re.sub(nojoke, '　', jk)
        return jk


def mars():
    return random.choice(botdb.marsmedia['photo'])
