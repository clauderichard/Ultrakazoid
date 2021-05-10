import os

def removeBackDirs(dirname):
    fos = dirname.split('/')
    i = 1
    while i < len(fos):
        if fos[i] == '..':
            del fos[i-1:i+1]
            i -= 1
        else:
            i += 1
    return str.join('/',fos)

def getAbsFilePath(filepath):
    return removeBackDirs(f"{os.getcwd()}/{filepath}")
