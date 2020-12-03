import os
import sys
import termios
import select
import tty
import ansi
import ansi.cursor
import ansi.colour.bg
import ansi.colour.fg

terminalSize = {
    "width": int(os.popen("stty size", "r").read().split()[1]),
    "height": int(os.popen("stty size", "r").read().split()[0])
}

class arrowKeys:
    UP = "\x1b[A"
    DOWN = "\x1b[B"
    LEFT = "\x1b[D"
    RIGHT = "\x1b[C"

def init():
    print(ansi.cursor.erase(2), end = "")

def setTopLineTabs(tabs, selectedTab = 0, page = "Challenger"):
    print(ansi.cursor.goto(1, 1), end = "")
    print(ansi.colour.bg.blue(ansi.colour.fg.white(" " * terminalSize["width"])))

    tabString = ""

    for i in range(0, len(tabs)):
        if i == selectedTab:
            tabString += ansi.colour.bg.white(ansi.colour.fg.black(" " + tabs[i] + " "))
        else:
            tabString += ansi.colour.bg.blue(ansi.colour.fg.white(" " + tabs[i] + " "))

    print(ansi.cursor.goto(1, 1) + ansi.colour.bg.blue(ansi.colour.fg.boldwhite(page) + ansi.colour.bg.blue(" ") + tabString))

def getKey(timeout = 1):
    fileno = sys.stdin.fileno()
    old = termios.tcgetattr(fileno)

    try:
        tty.setraw(fileno)

        i, o, e = select.select([sys.stdin], [], [], timeout)

        if i:
            char = sys.stdin.read(1)

            if char == "\x1B":
                char += sys.stdin.read(2)
        else:
            char = None
    finally:
        termios.tcsetattr(fileno, termios.TCSADRAIN, old)

    if char == "\x03":
        raise KeyboardInterrupt

    if char == "\x04":
        raise EOFError

    return char

def middle(text):
    return " " * (terminalSize["width"] // 2 - len(text) // 2) + text

def scrollable(items, y = 2, height = terminalSize["height"] - 2, scrollPos = 0):
    print("Scroll:", scrollPos)

    if scrollPos < 0:
        scrollPos = 0
    
    if scrollPos + height > len(items):
        scrollPos = max(len(items) - height, 0)

    for i in range(0, height):
        print(ansi.cursor.goto(y + i, 1) + " " * terminalSize["width"])

        if i + scrollPos < len(items):
            print(ansi.cursor.goto(y + i, 1) + str(items[i + scrollPos])[:terminalSize["width"]])
    
    return scrollPos

class Screen:
    def __init__(self):
        self.scrollPos = 0
    
    def render(self):
        print(ansi.cursor.erase(2), end = "")

    def update(self, key):
        if key == arrowKeys.UP:
            self.scrollPos -= 1
        elif key == arrowKeys.DOWN:
            self.scrollPos += 1

    def start(self):
        self.render()

        while True:
            self.update(getKey())

    def open(self, screen):
        screen.start()
        self.render()

class TabbedScreen(Screen):
    def __init__(self, tabs, selectedTab = 0, page = "Challenger"):
        super().__init__()

        self.tabs = tabs
        self.selectedTab = selectedTab

        self._previouslySelectedTab = None

    def updateTab(self, isChange = False):
        if self.selectedTab == self._previouslySelectedTab:
            return
        
        if isChange:
            self.scrollPos = 0

        setTopLineTabs(self.tabs, self.selectedTab)
        print(ansi.cursor.erase())

        self._previouslySelectedTab = self.selectedTab
    
    def forceTabUpdate(self):
        self._previouslySelectedTab = None

    def render(self):
        super().render()

        self.updateTab()

    def update(self, key):
        super().update(key)

        if key == arrowKeys.UP or key == arrowKeys.DOWN:
            self.forceTabUpdate()
            self.updateTab()
        elif key == arrowKeys.LEFT:
            self.selectedTab -= 1

            if self.selectedTab < 0:
                self.selectedTab = len(self.tabs) - 1
        
            self.updateTab(True)
        elif key == arrowKeys.RIGHT:
            self.selectedTab += 1

            if self.selectedTab > len(self.tabs) - 1:
                self.selectedTab = 0
            
            self.updateTab(True)