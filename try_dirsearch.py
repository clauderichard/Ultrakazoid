import os
import re

################################################

def allFiles(dirpath="."):
    for x in os.scandir(dirpath):
        if x.is_dir():
            yield from allFiles(f"{dirpath}/{x.name}")
        else:
            yield f"{dirpath}/{x.name}"
            
def allFunctions(filename):
    with open(filename,"r") as fil:
        for line in fil.readlines():
            s = line.lstrip()
            if s[0:4] == "def ":
                ls = s[4:].split("(")
                if len(ls)>1:
                    fun = ls[0]
                    if fun[0:2] != "__":
                        yield fun

def findString(filename,searchString):
    with open(filename,"r") as fil:
        i = 1
        for line in fil.readlines():
            s = line.lstrip()
            if searchString in s:
                yield i
            i += 1

################################################

def findStrings(searchString):
    for f in allFiles("music_ukz/ukz"):
        ls = list(findString(f,searchString))
        if ls:
            print(f"  {f}")
            for l in ls:
                print(f"    {l}")
        print(f)
        for f in allFunctions(f):
            print(f"  {f}")

def findFuncs():
    for f in allFiles("music_ukz/ukz"):
        print(f)
        for f in allFunctions(f):
            print(f"  {f}")

def findFuncs_try():
    m = re.compile(r'def [a-zA-Z0-9]+').search("t def func(c): c  def gc(u)")
    print(m)
    if m is not None:
        print(m.group(0)[4:])
    
################################################

findStrings("floor")

