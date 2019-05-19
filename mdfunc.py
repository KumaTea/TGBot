import random


def randomjoke():
    jkfl = random.choice(range(7))
    with open('joke/soviet' + str(jkfl), 'r', encoding='utf-8') as joke:
        jk = random.choice(list(joke)).replace('br', '\n')
        return jk
