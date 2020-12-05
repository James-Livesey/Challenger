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
                self.open(RunningProcessScreen(newProcess))
            except FileNotFoundError:
                ui.setBottomLineError("Cannot find executable at given path")
                print(ansi.cursor.goto(6, 1), end = "")
    
    def goodbye(self):
        raise KeyboardInterrupt

class KeyboardShortcutsScreen(ui.OverlayScreen):
    def __init__(self, shortcutsPath):
        super().__init__()

        shortcutsFile = open(shortcutsPath, "r")
        self.shortcuts = shortcutsFile.read().split("\n")

        shortcutsFile.close()
    
    def render(self):
        super().render()

        for i in range(self.bottom, self.bottom + self.height - 2):
            if i - self.bottom < len(self.shortcuts):
                print(ansi.cursor.goto(ui.terminalSize["height"] - self.height - self.bottom + i, 3) + ansi.colour.bg.blue(ansi.colour.fg.white(self.shortcuts[i - self.bottom][:(ui.terminalSize["width"] - 4)])))

class RunningProcessScreen(ui.TabbedScreen):
    def __init__(self, process):
        super().__init__(["Status", "Data", "Graph"], 0, "Process")

        self.process = process
        self.page = self.process.getShortName()
        self.displayDataAsTable = True
        self.autoscrollToBottom = True

    def renderData(self):
        if self.displayDataAsTable:
            if len(self.process.data) > 1:
                print(ansi.cursor.goto(2, 1) + " " * ui.terminalSize["width"])
                print(ansi.cursor.goto(2, 1) + ansi.colour.fg.bold(("  | " + ui.constructTableLine(self.process.data[0]["values"], self.process.tableColumnLengths))[:ui.terminalSize["width"]] + " |"))
                
                self.scrollPos = ui.scrollable(
                    self.process.data[1:],
                    y = 3,
                    height = ui.terminalSize["height"] - 3,
                    scrollPos = self.scrollPos,
                    lineFunction = lambda line: processing.renderInCategoryColour(
                        processing.getCategorySymbol(line["category"]) + " | " + ui.constructTableLine(line["values"], self.process.tableColumnLengths) + " | " + ansi.colour.fg.darkgrey(processing.formatTimestamp(line["timestamp"])),
                        line["category"]
                    )
                )

                if self.autoscrollToBottom:
                    self.scrollPos = len(self.process.data[1:])
        else:
            self.scrollPos = ui.scrollable(
                self.process.data,
                scrollPos = self.scrollPos,
                lineFunction = lambda line: line["raw"]
            )
        
        ui.setBottomLineStatus(
            ("[M]" if self.displayDataAsTable else " M ") +
            ("[A]" if self.autoscrollToBottom else " A ") +
            " | Lines: {}".format(len(self.process.data))
        )

    def updateTab(self, isChange = False):
        super().updateTab(isChange)

        if self.selectedTab == 1:
            self.renderData()
    
    def update(self, key):
        super().update(key)

        self.process.update()

        if key == "m":
            self.displayDataAsTable = not self.displayDataAsTable
        
        if key == "a":
            self.autoscrollToBottom = not self.autoscrollToBottom
        
        if key == "?":
            self.open(KeyboardShortcutsScreen("docs/shortcuts/data.txt"))

        if self.process.hasNewData:
            if self.selectedTab == 1:
                self.renderData()