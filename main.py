import ansi.cursor

import screens

try:
    welcomeScreen = screens.WelcomeScreen()

    welcomeScreen.start()
except KeyboardInterrupt:
    print(ansi.cursor.goto(1, 1) + ansi.cursor.erase(0), end = "")