"""
"""
# Standard Imports
import logging
from multiprocessing import Process
from multiprocessing.connection import PipeConnection

# Third Party Imports 
import keyboard 
import webview

# Internal Imports


# TODO: Support settings to get the hotkeys
TRIGGER_HOTKEY = "capslock"
# NOTE: We should not need quit hotkey, we will use the app icon tro handle this
# or have an exit command in the application
QUIT_HOTKEY = "ctrl+e"


def onQuit(connection: PipeConnection):
    logger = logging.getLogger("QUICKACCESS")
    logger.debug("Quit hotkey is pressed, sending the request to exit the application")
    connection.send("exit")
    

def onTriggerPress(connection: PipeConnection):
    logger = logging.getLogger("QUICKACCESS")
    connection.send("ShowCommandPrompt")
    logger.debug(f"{TRIGGER_HOTKEY} was pressed!")
    

def onTriggerRelease(connection: PipeConnection):
    logger = logging.getLogger("QUICKACCESS")
    connection.send("HideCommandPrompt")
    logger.debug(f"{TRIGGER_HOTKEY} was released!")
    

def listenKeyboard(connection: PipeConnection):
    logger = logging.getLogger("QUICKACCESS")
    logger.debug(f"Start listening keyboard")
    keyboard.add_hotkey(TRIGGER_HOTKEY, onTriggerPress, args=(connection,), suppress=True, trigger_on_release=False)
    keyboard.add_hotkey(TRIGGER_HOTKEY, onTriggerRelease, args=(connection,), suppress=True, trigger_on_release=True)
    keyboard.add_hotkey(QUIT_HOTKEY, onQuit, args=(connection,), suppress=True)
    while True:
        # Wait for the next event.
        _ = keyboard.read_event()
    

if __name__ == "__main__":
    pass 
