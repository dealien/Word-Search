def load_words():
    with open('wordlist.txt') as f:
        return  f.read().splitlines()

def boardgen(width, height):
    wordlist=load_words()
    board=[]
    for i in range(height):
        board.append([None for _ in range(width)])
    print(board)


boardgen(20,40)