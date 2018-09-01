import random
from pprint import pprint

width = 20
height = 20

if width < 20:
    width = 20
if height < 20:
    height = 20


class Cell:
    """Contains information about a single cell in
    the board"""

    def __init__(self, letter, **kwargs):
        self.letter = letter
        self.is_word = False
        self.is_beginning = False
        self.d = None  # Word direction


# @property
# def dump(self):
#     return {
#         'name': self.name,
#         'model': self.model,
#         'owner': self.owner,
#         'hull': self.hull,
#         'shields': self.shields,
#         'power': self.power,
#         'shieldstatus': self.shieldstatus
#     }


def load_words():
    global width, height
    with open('wordlist.txt') as f:
        words = f.read().splitlines()
    maxlength = min(width - 9, height - 9)
    minlength = 5
    wordlist = []
    for word in words:
        if minlength < len(word) < maxlength:
            wordlist.append(word)
    return wordlist


def boardgen(w, h):
    wordlist = load_words()
    board = []
    for i in range(h):
        board.append([Cell(random.choice(list('abcdefghijklmnopqrstuvwxyz'))) for _ in range(w)])

    wordcount = (w * h) * 0.05
    added = []
    while len(added) != wordcount:
        word = random.choice(wordlist)
        d = random.choice(['v', 'h'])  # The direction of the word (vertical or horizontal)
        y = 0
        x = 0
        while y + len(word) > len(board) or y is 0:
            y = int(random.choice(range(h)))
        while x + len(word) > len(board) or x is 0:
            x = int(random.choice(range(w)))
        c = board[y][x]
        xy = [x, y]
        if c.is_word is False:
            # TODO: Also check other qualifying factors
            a = True
            wl = len(word)
            while a is True and wl > 0:
                c = board[y][x]
                # TODO: Make the following if-statements allow words to overlap the beginnings of words going in the other direction
                if c.d is not d and d is 'v':
                    y += 1
                elif c.d is not d and d is 'h':
                    x += 1
                wl -= 1
            if a is True:
                x = xy[0]
                y = xy[1]
                first = True
                for j in list(word):
                    if first is True:
                        board[y][x] = Cell(letter=j, is_word=True, is_beginning=True, d=d)
                    else:
                        board[y][x] = Cell(letter=j, is_word=True, is_beginning=False, d=d)
                    first = False
                    if d is 'v':
                        y += 1
                    if d is 'h':
                        x += 1
            added.append(word)
    return board, added


def draw_board(board, words):
    print()
    for i in board:
        o = ''
        for j in i:
            o += j.letter
        print(''.join(o))
    print()
    print(str(len(words))+' words hidden:\n' + ', '.join(words))


ginfo = [''] * 2
ginfo[0], ginfo[1] = boardgen(width, height)
draw_board(ginfo[0], ginfo[1])
