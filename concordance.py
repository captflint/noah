import lzma
with lzma.open('webster.txt.xz', 'rt') as w:
    webster = w.read()
concordance = []
deduplist = []
line = ''
currentchar = 0
lastnewline = 0
for char in webster:
    if char == '\n':
        if line.isupper() and line not in deduplist:
            concordance.append((lastnewline, line))
            deduplist.append(line)
        lastnewline = currentchar
        line = ''
    else:
        line += char
    currentchar += 1
    if currentchar % 100000 == 0:
        print(currentchar / len(webster), len(concordance), concordance[-1])
with open('index.txt', 'wt') as out:
    out.write(str(concordance))
