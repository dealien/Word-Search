from shutil import copyfile

import wordsearch

webfolder = './web/'


def arr_to_html_table(arr, id=None):
    if id is not None:
        t = '<table id=' + str(id) + '>'
    else:
        t = '<table>'
    for sarr in arr:
        t += '<tr>'
        for j in sarr:
            t += '<td>' + j.letter + '</td>\n'
        t += '</tr>\n'
    t += '</table>'
    return t


def generate_html():
    copyfile('cwstyle.css', webfolder + 'css/cwstyle.css')
    with open('crossword_template.html', 'r') as f:
        d = f.readlines()
    s = ''.join(d)

    board, wordlist = wordsearch.start_game()
    c = s.format(arr_to_html_table(board, 'board-table'), '<p>' + '</p><p>'.join(wordlist) + '</p>')

    f = open(webfolder + 'crossword.html', 'w')
    f.write(c)
    f.close()
    return True
