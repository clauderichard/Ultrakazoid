import cProfile
import pstats
import os

def benchmarkScript(scriptCode,tempFileName='restats'):
    cProfile.run(scriptCode, tempFileName)
    p = pstats.Stats(tempFileName)
    os.remove(tempFileName)
    return p.strip_dirs().sort_stats('cumtime')


p = benchmarkScript("import sitscripts.AsteroidPunching")

p.print_stats(50)
#p.print_callers(20)
