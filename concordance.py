import lzma
with lzma.open('webster.txt.xz', 'rt') as w:
    webster = w.read()
concordance = []
deduplist = []
word = ''
currentchar = 0
for char in webster:
    if char in '., \n':
        if len(word) == 0:
            continue
        else:
            if word.upper() not in deduplist:
                wordindex = webster.find('\n' + word.upper() + '\n')
                if wordindex >= 0:
                    concordance.append((word.upper(), wordindex))
                    deduplist.append(word.upper())
                else:
                    deduplist.append(word.upper())
            word = ''
    else:
        word += char
    currentchar += 1
    if currentchar % 10000 == 0:
        print(currentchar / len(webster), len(concordance), len(deduplist))
concordance.sort()
print(concordance)
