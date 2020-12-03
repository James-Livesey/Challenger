import os
import ansi
import ansi.cursor
import ansi.colour.bg
import ansi.colour.fg

terminalSize = {
    "width": int(os.popen("stty size", "r").read().split()[1]),
    "height": int(os.popen("stty size", "r").read().split()[0])
}

def init():
    print(ansi.cursor.erase(2), end = "")

def setTopLineTabs(tabs, selectedTab = 0):
    print(ansi.cursor.goto(1, 1), end = "")
    print(ansi.colour.bg.blue(ansi.colour.fg.white(" " * terminalSize["width"])))

    tabString = ""

    for i in range(0, len(tabs)):
        if i == selectedTab:
            tabString += ansi.colour.bg.white(ansi.colour.fg.black(" " + tabs[i] + " "))
        else:
            tabString += ansi.colour.bg.blue(ansi.colour.fg.white(" " + tabs[i] + " "))

    print(ansi.cursor.goto(1, 1) + ansi.colour.bg.blue(
        ansi.colour.fg.boldwhite("Challenger ") +
        tabString
    ), end = "")