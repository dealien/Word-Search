import random


class Cell:
    """Contains information about a single cell in
    the board"""

    def __init__(self, letter, is_word=False, is_beginning=False, d=None):
        self.letter = letter
        self.is_word = is_word
        self.is_beginning = is_beginning
        self.d = d  # Word direction

    def __repr__(self):
        return str({
            'letter': self.letter,
            'is_word': self.is_word,
            'is_beginning': self.is_beginning,
            'd': self.d
        })

    def __str__(self):
        return str(self.letter)


def load_words(w, h):
    with open('./lists/wordlist.txt') as f:
        words = f.read().splitlines()
    maxlength = min(w, h)
    minlength = 4
    wordlist = []
    for word in words:
        if minlength < len(word) < maxlength:
            wordlist.append(word)
    return wordlist


def boardgen(w, h, max=None):
    wordlist = load_words(w, h)
    board = []
    for i in range(h):
        board.append([Cell(random.choice(list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'))) for _ in range(w)])
    if max is None:
        wordcount = (w * h) * 0.05
    else:
        wordcount = max
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

        a = True
        wl = len(word)
        while a is True and wl > 0:
            c = board[y][x]
            if c.is_word is True and c.letter.lower() is not word[len(word) - wl].lower():
                a = False
                # print('Word does not fit')
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
                    board[y][x] = Cell(j.upper(), True, True, d)
                else:
                    board[y][x] = Cell(j.upper(), True, False, d)
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


def start_game(w=20, h=20, max=None):
    a, b = boardgen(w, h, max)
    # draw_board(a, b)
    return a, b
