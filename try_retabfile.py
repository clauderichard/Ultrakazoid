
def funcEachLine(fun,filename):
    with open(filename,'r') as rf:
        for line in rf.readlines():
            yield fun(line)

def retab(filename):
    filenameWithExt = filename + '.py'
    newfilenameWithExt = filename + '.py'
    def fun(line):
        numspaces = 0
        for i in range(0,len(line)):
            if line[i]==' ':
                numspaces += 1
            else:
                break
        newlin = ' ' * (numspaces*2) + line[numspaces:]
        return newlin
    inputLines = list(funcEachLine(fun,filenameWithExt))
    with open(newfilenameWithExt,'w') as outf:
        for newlin in inputLines:
            outf.write(newlin)

#retab('test_ukz/test_ukzlang/test_uk_base')
