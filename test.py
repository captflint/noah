import lzma
with lzma.open('webster.txt.xz', 'rt') as w:
    webster = w.read()
#query = input('Enter a word to look up: ')
query = 'test'
query = '\n' + query.upper() + '\n'
start = webster.find(query)
if start == -1:
    print('Word not found')
else:
    print(webster[start:start + 400])



