import os

def gotoscriptdir():
    spath = __file__
    sdirs = spath.split('\\')
    sdirs = sdirs[0:len(sdirs)-1]
    sdir = ''
    for d in sdirs:
        sdir += d + '\\'
    os.chdir(sdir)

def gotoscriptdir2():
    spath = __file__
    a = spath.index('test_ukz')
    sdir = spath[0:a]
    os.chdir(sdir)

def printStuff():
    print('--------------------------------')
    print(os.getcwd())
    print(__file__)
    print(os.curdir)
    print(list(os.scandir(os.curdir)))
    print('--------------------------------')

printStuff()
os.chdir("..")
printStuff()
gotoscriptdir()
printStuff()
gotoscriptdir2()
printStuff()
