import random

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


def load_words():
    global width, height
    with open('./lists/wordlist.txt') as f:
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
        board.append([Cell(random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))) for _ in range(w)])
    wordcount = (w * h) * 0.05
    added = []
    while len(added) != wordcount and len(wordlist) > 0:
        word = random.choice(wordlist)
        wordlist.remove(word)
        d = random.choice(['v', 'h'])  # The direction of the word (vertical or horizontal)
        y = 0
        x = 0
        while y + len(word) > len(board) or y is 0:
            y = int(random.choice(range(h)))
        while x + len(word) > len(board) or x is 0:
            x = int(random.choice(range(w)))
        c = board[y][x]
        xy = [x, y]
        if c.is_word is False:  # TODO: Also check other qualifying factors
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
                        board[y][x] = Cell(letter=j.upper(), is_word=True, is_beginning=True, d=d)
                    else:
                        board[y][x] = Cell(letter=j.upper(), is_word=True, is_beginning=False, d=d)
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
    print(str(len(words)) + ' words hidden:\n' + ', '.join(words))


def start_game(w=width, h=height):
    a, b = boardgen(w, h)
    draw_board(a, b)
    return a, b
