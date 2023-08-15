"""
"""
# Standard Imports
import logging
from multiprocessing import Process
from multiprocessing.connection import PipeConnection
import os

# Third Party Imports 
import webview
import keyboard 

# Internal Imports

# TODO: Support settings to get the hotkeys
TRIGGER_HOTKEY = "capslock"
# NOTE: We should not need quit hotkey, we will use the app icon tro handle this
# or have an exit command in the application
QUIT_HOTKEY = "ctrl+e"

class App:
    stopRequested: bool = False
    active: bool = False
    connectionToSend: PipeConnection

    def start(self, connectionToSend: PipeConnection):
        """ We start both the keyboard listener and the webview applications """
        logger = logging.getLogger("QUICKACCESS")
        logger.setLevel(os.environ.get("LOGLEVEL", "DEBUG"))
        logger.info("START")
        self.connectionToSend = connectionToSend
        commandPrompt = Process(target=listenKeyboard, args=(connectionToSend, self), daemon=True)
        commandPrompt.start()
    
    def stop(self):
        """ Stop the application """
        logger = logging.getLogger("QUICKACCESS")
        logger.info("Stop Requested Ending the application")
        self.stopRequested = True 
        

def onQuit(app: App):
    logger = logging.getLogger("QUICKACCESS")
    logger.debug("Quit hotkey is pressed, sending the request to exit the application")
    app.connectionToSend.send("exit")
    

def onTriggerPress(app: App):
    logger = logging.getLogger("QUICKACCESS")
    if app.active:
        return 
    app.active = True
    app.connectionToSend.send("ShowCommandPrompt")
    logger.debug(f"{TRIGGER_HOTKEY} was pressed!")
    

def onTriggerRelease(app: App):
    logger = logging.getLogger("QUICKACCESS")
    if not app.active:
        return 
    app.active = False
    app.connectionToSend.send("HideCommandPrompt")
    logger.debug(f"{TRIGGER_HOTKEY} was released!")
    

def listenKeyboard(connectionToSend: PipeConnection, app: App):
    logging.basicConfig(level="DEBUG")
    logger = logging.getLogger("QUICKACCESS")
    logger.debug(f"Start listening keyboard for app {app}")
    keyboard.add_hotkey(TRIGGER_HOTKEY, onTriggerPress, args=(app,), suppress=True, trigger_on_release=False)
    keyboard.add_hotkey(TRIGGER_HOTKEY, onTriggerRelease, args=(app,), suppress=True, trigger_on_release=True)
    keyboard.add_hotkey(QUIT_HOTKEY, onQuit, args=(app,), suppress=True)
    while not app.stopRequested:
        # Wait for the next event.
        _ = keyboard.read_event()
    logger.debug("Keyboard event loop is ended")


def main():
    pass


if __name__ == "__main__":
    pass 
