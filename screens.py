import ansi
import ansi.cursor
import ansi.colour.fg

import ui
import processing

class WelcomeScreen(ui.TabbedScreen):
    def __init__(self):
        super().__init__(["Welcome", "Help", "About"])

        helpFile = open("docs/help.txt")
        self.helpText = helpFile.read().split("\n")

        helpFile.close()
    
    def updateTab(self, isChange = False):
        super().updateTab(isChange)

        if self.selectedTab == 0:
            print(ansi.colour.fg.bold(ui.middle("Welcome to Challenger!")))
            print("")
            print(ui.middle("Press Enter to launch a process"))
            print(ui.middle("Use Left and Right to change tabs"))
            print(ui.middle("Press Ctrl + C to exit"))
        elif self.selectedTab == 1:
            self.scrollPos = ui.scrollable(self.helpText, scrollPos = self.scrollPos)
    
    def update(self, key):
        super().update(key)

        if key == "\x0D":
            self.selectedTab = 0
            self.updateTab()

            print(ansi.cursor.goto(2, 1) + ansi.cursor.erase())
            print("> Executable path:")
            print("  File to log output to:")

            print(ansi.cursor.goto(3, 28), end = "")
            
            executable = input()

            print(ansi.cursor.goto(3, 1) + " ", end = "")
            print(ansi.cursor.goto(4, 1) + ">", end = "")
            print(ansi.cursor.goto(4, 28), end = "")
            
            outputFile = input()

            newProcess = processing.Process(executable, outputFile)

            try:
                newProcess.start()

                processing.processes.append(newProcess)

                runningProcessScreen = RunningProcessScreen(newProcess)

                runningProcessScreen.start()
            except FileNotFoundError:
                ui.setBottomLineError("Cannot find executable at given path")
                print(ansi.cursor.goto(6, 1), end = "")

class RunningProcessScreen(ui.TabbedScreen):
    def __init__(self, process):
        super().__init__(["Status", "Data", "Graph"], 0, "Process")

        self.process = process
        self.page = self.process.getShortName()
        self._lastProcessRead = None
    
    def updateTab(self, isChange = False):
        super().updateTab(isChange)

        if self.selectedTab == 1:
            self._lastProcessRead = None
    
    def update(self, key):
        super().update(key)

        processRead = self.process.read().decode().split("\n")

        if processRead != self._lastProcessRead:
            if self.selectedTab == 1:
                self.scrollPos = ui.scrollable(processRead, scrollPos = self.scrollPos)

                ui.setBottomLineStatus("Lines: {}".format(len(processRead)))

            self._lastProcessRead = processRead