import lzma
with lzma.open('webster.txt.xz', 'rt') as w:
    webster = w.read()
query = input('Enter a word to look up: ')
query = '\n' + query.upper() + '\n'
start = webster.find(query)
if start == -1:
    print('Word not found')
else:
    while True:
        line = ''
        while webster[start] != '\n':
            line += webster[start]
            start += 1
        input(line)
        line = ''
        start += 1
