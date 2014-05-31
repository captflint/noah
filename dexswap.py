from oldindex import oldindex

words, indices = zip(*oldindex)
newindex = zip(indices, words)
newindex = list(newindex)
newindex.sort()
with open('index.txt', 'wt') as outfile:
    outfile.write(str(newindex))
