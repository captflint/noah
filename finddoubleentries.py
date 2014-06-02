from index import index
doubleentries = []
for item in index:
    if '; ' in item[1]:
        templist = []
        tempstr = ''
        skipnext = False
        for char in item[1]:
            if skipnext:
                skipnext = False
                continue
            if char == ';':
                templist.append(tempstr)
                tempstr = ''
                skipnext = True
            else:
                tempstr += char
        templist.append(tempstr)
        doubleentries.append((item[1], templist))
        templist = []
with open('doubleentries.py', 'wt') as outfile:
    outfile.write('doubleentries = ' + str(doubleentries))
