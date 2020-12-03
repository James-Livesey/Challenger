import ui
import ansi
import ansi.colour.fg

class WelcomeScreen(ui.TabbedScreen):
    def __init__(self):
        super().__init__(["Welcome", "Help", "About"])

        helpFile = open("docs/help.txt")
        self.helpText = helpFile.read().split("\n")

        helpFile.close()
    
    def updateTab(self, isChange = False):
        super().updateTab()

        if self.selectedTab == 0:
            print(ansi.colour.fg.bold(ui.middle("Welcome to Challenger!")))
            print("")
            print(ui.middle("Press Enter to launch a process"))
            print(ui.middle("Use Left and Right to change tabs"))
        elif self.selectedTab == 1:
            self.scrollPos = ui.scrollable(self.helpText, scrollPos = self.scrollPos)