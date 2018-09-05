import logging
import random

import coloredlogs

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', fmt='%(asctime)s.%(msecs)03d %(name)s[%(process)d] %(levelname)s %(message)s')


class Cell:
    """Contains information about a single cell in
    the board"""

    def __init__(self, letter, is_word=False, is_beginning=False, d=None):
        if d is None:
            d = [False, False]
        self.letter = letter
        self.is_word = is_word
        self.is_beginning = is_beginning
        self.d = d

    def __repr__(self):
        return str({
            'letter': self.letter,
            'is_word': self.is_word,
            'is_beginning': self.is_beginning,
            'd': self.d
        })

    def __str__(self):
        return str(self.letter)

    @property
    def h(self):
        return self.d[0]

    @h.setter
    def h(self, h):
        self.d = [h, self.d[1]]

    @property
    def v(self):
        return self.d[1]

    @v.setter
    def v(self, v):
        self.d = [self.d[0], v]


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
        # While the number of added words is less than the max and the word list is not empty
        word = random.choice(wordlist)
        wordlist.remove(word)
        d = random.choice([[True, False], [False, True]])  # The direction of the word (horizontal or vertical)
        y = 0
        x = 0
        while y + len(word) > len(board) or y is 0:
            y = int(random.choice(range(h)))
        while x + len(word) > len(board) or x is 0:
            x = int(random.choice(range(w)))
        xy = [x, y]

        allowed = True
        wl = len(word)
        while allowed is True and wl > 0:
            # Loops over each cell the candidate word would cross and verify its availability
            c = board[y][x]
            if c.is_word is True and c.letter.lower() is not word[len(word) - wl].lower():
                # If the cell is part of a word and the letters don't match, break
                allowed = False
                logger.warning('Word does not fit: %s', word)
                break

            if d[0] is True and c.h is False:
                # If the candidate is horizontal and the cell is not already part of a horizontal word, continue
                x += 1
            elif d[1] is True and c.v is False:
                # If the candidate is vertical and the cell is not already part of a vertical word, continue
                y += 1
            wl -= 1
        if allowed is True:
            logger.info('Word allowed: %s', word)
            # If word placement was allowed in all cells, continue to add the word to each cell
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
    logger.info(str(len(words)) + ' words hidden:\n' + ', '.join(words))


def start_game(w=20, h=20, max=None):
    a, b = boardgen(w, h, max)
    # draw_board(a, b)
    return a, b
