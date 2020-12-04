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
    UP = "\x1B[A"
    DOWN = "\x1B[B"
    LEFT = "\x1B[D"
    RIGHT = "\x1B[C"

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

def setBottomLineStatus(status):
    print(ansi.cursor.goto(terminalSize["height"], 1), end = "")
    print(ansi.colour.bg.blue(ansi.colour.fg.white(" " * terminalSize["width"])), end = "")

    print(ansi.cursor.goto(terminalSize["height"]) + ansi.colour.bg.blue(ansi.colour.fg.white(status[:terminalSize["width"]])) + ansi.cursor.goto(terminalSize["height"] - 2))

def setBottomLineError(status):
    print(ansi.cursor.goto(terminalSize["height"], 1), end = "")
    print(ansi.colour.bg.red(ansi.colour.fg.white(" " * terminalSize["width"])), end = "")

    print(ansi.cursor.goto(terminalSize["height"]) + ansi.colour.bg.red(ansi.colour.fg.white(status[:terminalSize["width"]])) + ansi.cursor.goto(terminalSize["height"] - 2))

def getKey(timeout = 1):
    fileno = sys.stdin.fileno()
    old = termios.tcgetattr(fileno)

    try:
        tty.setraw(fileno)

        i = select.select([sys.stdin], [], [], timeout)[0]

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

def scrollable(items, y = 2, height = terminalSize["height"] - 2, scrollPos = 0, lineFunction = lambda line: line):
    if scrollPos < 0:
        scrollPos = 0
    
    if scrollPos + height > len(items):
        scrollPos = max(len(items) - height, 0)

    for i in range(0, height):
        print(ansi.cursor.goto(y + i, 1) + " " * terminalSize["width"])

        if i + scrollPos < len(items):
            print(ansi.cursor.goto(y + i, 1) + str(lineFunction(items[i + scrollPos]))[:terminalSize["width"]])
    
    return scrollPos

def constructTableLine(items, lengths, delimiter = " | "):
    result = ""

    while len(items) > len(lengths):
        lengths.append(10)
    
    while len(lengths) > len(items):
        items.append("")

    for i in range(0, len(items)):
        if len(items[i]) > lengths[i]:
            result += items[i][:lengths[i]]
        else:
            result += items[i] + (" " * (lengths[i] - len(items[i])))
        
        if i < len(items) - 1:
            result += delimiter
    
    return result

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
        self.page = page

        self._previouslySelectedTab = None

    def updateTab(self, isChange = False):
        if self.selectedTab == self._previouslySelectedTab:
            return
        
        if isChange:
            self.scrollPos = 0

        setTopLineTabs(self.tabs, self.selectedTab, self.page)
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