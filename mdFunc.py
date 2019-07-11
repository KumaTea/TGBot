import random


def random_joke():
    joke_file = random.choice(range(7))
    with open('joke/soviet' + str(joke_file), 'r', encoding='utf-8') as joke:
        jk = random.choice(list(joke)).replace('br', '\n')
        """
        if nojo:
            nojoke = re.compile('[^0-9\\n，。、？！（…“”：；‘’《》）]|_')
            jk = re.sub(nojoke, '　', jk)
        """
        return jk


def sysu_joke():
    with open('joke/sysu0', 'r', encoding='utf-8') as joke:
        jk = random.choice(list(joke)).replace('br', '\n')
        return jk
