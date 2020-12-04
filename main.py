import ansi.cursor

import screens
import processing

try:
    welcomeScreen = screens.WelcomeScreen()

    welcomeScreen.start()
except KeyboardInterrupt:
    for process in processing.processes:
        process.stop()
    
    print(ansi.cursor.goto(1, 1) + ansi.cursor.erase(0), end = "")