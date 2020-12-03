import ui
import ansi
import ansi.cursor
import ansi.colour.fg

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
            input()

            print(ansi.cursor.goto(3, 1) + " ", end = "")
            print(ansi.cursor.goto(4, 1) + ">", end = "")
            print(ansi.cursor.goto(4, 28), end = "")
            input()

            ui.setBottomLineError("James hasn't gotten around to coding this bit yet")
            print(ansi.cursor.goto(6, 1), end = "")