import subprocess

processes = []

class Process:
    def __init__(self, executable, outputFile):
        self.executable = executable
        self.outputFile = outputFile

        self.runningProcess = None
    
    def start(self):
        self.runningProcess = subprocess.Popen(self.executable, stdout = open(self.outputFile, "wb"))
    
    def read(self):
        outputFileOpen = open(self.outputFile, "rb")
        outputFileData = outputFileOpen.read()

        outputFileOpen.close()

        return outputFileData