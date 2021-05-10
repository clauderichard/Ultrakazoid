import os
import unittest
from ukz.config import log,UkzConfig

class TestScripts1(unittest.TestCase):

################
# Helper methods

    def __readBinFileContent(self,filename):
        content1 = bytearray(b'')
        with open(f"{filename}",'br') as fil:
            content1 = fil.read()
        return content1

    def __readScriptCode(self,scriptName):
        scriptCode = ""
        with open(f"{scriptName}.py",'r') as fil:
            scriptCode = fil.read()
        return scriptCode
            
    def __chdirTestUkzParent(self):
        spath = __file__
        a = spath.index('test_ukz')
        sdir = spath[0:a]
        os.chdir(sdir)

    def scriptTest(self,scriptName,midiName):
        UkzConfig.logEnabled = False
        
        __import__(f"sitscripts.{scriptName}")
        
        cdir = os.getcwd()
        self.__chdirTestUkzParent()
        expectedBin = self.__readBinFileContent(f"good_midi_files/{midiName}.mid")
        os.chdir(cdir)
        actualBin = self.__readBinFileContent(f"{UkzConfig.outputMidiFolder}/{midiName}.mid")
        self.assertEqual(expectedBin,actualBin)

################
# Tests

    def test_scriptOutput(self):
        for scriptName,midiName in [
          ["AsteroidPunching","Asteroid Punching"],
          ["onenote","onenote"],
          ["nostsun","nostsun"],
          ["choirsong","nostsun"],
          ["dumbthingy","dumbthingy"],
          ["fastnote","fastnote"],
          ["gradreverts","gradreverts"],
          ["pipesong","pipesong"],
          ["saxnosense","saxnosense"],
        ]:
            with self.subTest(scriptName):
                self.scriptTest(scriptName,midiName)
                print('S',end='')

################################
