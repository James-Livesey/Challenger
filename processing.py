import subprocess
import pathlib

processes = []

class Process:
    def __init__(self, executable, outputFile):
        self.executable = executable
        self.outputFile = outputFile

        self.runningProcess = None
    
    def start(self):
        pathlib.Path(self.outputFile).parent.mkdir(parents = True, exist_ok = True)

        self.runningProcess = subprocess.Popen(self.executable, stdout = open(self.outputFile, "wb"))
    
    def stop(self):
        self.runningProcess.kill()

        self.runningProcess = None
    
    def read(self):
        outputFileOpen = open(self.outputFile, "rb")
        outputFileData = outputFileOpen.read()

        outputFileOpen.close()

        return outputFileData
    
    def getShortName(self):
        return self.executable.split("/")[-1]