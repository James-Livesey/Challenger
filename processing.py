import subprocess
import pathlib
import ansi
import ansi.colour

processes = []

def getCategorySymbol(category):
    if category == 0:
        return " "
    elif category == "#":
        return "#"
    else:
        return str(category)

def renderInCategoryColour(text, category):
    if category == 0:
        return ansi.colour.fg.default(text)
    elif category == -1:
        return ansi.colour.fg.grey(text)
    elif (category - 1) % 4 == 0:
        return ansi.colour.fg.red(text)
    elif (category - 2) % 4 == 0:
        return ansi.colour.fg.green(text)
    elif (category - 3) % 4 == 0:
        return ansi.colour.fg.blue(text)
    elif category % 4 == 0:
        return ansi.colour.fg.yellow(text)

def parseCommaSeparatedValues(line):
    category = 0
    result = [""]
    position = 0
    inString = False
    hadEscapedQuote = False

    while position < len(line):
        if position == 0 and line[position] == "#":
            if len(line) > 2 and line[position + 1] in "123456789":
                category = int(line[position + 1])
                position += 3
            else:
                category = -1
                position += 1
        elif line[position] == "," and not inString:
            result.append("")

            position += 1
        elif line[position] == "\"":
            inString = not inString

            if position > 0 and line[position - 1] == "\"" and not hadEscapedQuote:
                result[-1] += "\""
                hadEscapedQuote = True
            else:
                hadEscapedQuote = False
            
            position += 1
        else:
            result[-1] += line[position]
            position += 1
    
    result = [i.strip() for i in result]
    
    if result == [""]:
        category = -1

    return {"raw": line, "category": category, "values": result}

class Process:
    def __init__(self, executable, outputFile):
        self.executable = executable
        self.outputFile = outputFile
        self.data = []
        self.tableColumnLengths = []
        self.hasNewData = False

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
    
    def update(self):
        rawData = self.read().decode().split("\n")

        if len(rawData) == len(self.data):
            self.hasNewData = False

            return

        for i in range(len(self.data), len(rawData)):
            if rawData[i].strip() == "":
                continue

            values = parseCommaSeparatedValues(rawData[i])

            self.data.append(values)

            while len(values["values"]) > len(self.tableColumnLengths):
                self.tableColumnLengths.append(0)

            for j in range(0, len(values["values"])):
                self.tableColumnLengths[j] = max(self.tableColumnLengths[j], len(values["values"][j]))
        
        self.hasNewData = True
    
    def getShortName(self):
        return self.executable.split("/")[-1]