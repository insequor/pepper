"""
"""
# Standard Imports
import logging
from multiprocessing import Process
from multiprocessing.connection import PipeConnection
import os 

# Third Party Imports 
import keyboard 
import webview
import pywinauto.keyboard
# Internal Imports


# TODO: Support settings to get the hotkeys
TRIGGER_HOTKEY = "capslock"
# NOTE: We should not need quit hotkey, we will use the app icon tro handle this
# or have an exit command in the application
QUIT_HOTKEY = "ctrl+e"


def onQuit(connection: PipeConnection):
    logger = logging.getLogger("QUICKACCESS")
    logger.debug("Quit hotkey is pressed, sending the request to exit the application")
    connection.send({"key": "exit"})
    

def onTriggerPress(connection: PipeConnection):
    logger = logging.getLogger("QUICKACCESS")
    connection.send({"key": "ShowCommandPrompt"})
    logger.debug(f"{TRIGGER_HOTKEY} was pressed!")
    return True
    

def onTriggerRelease(connection: PipeConnection):
    logger = logging.getLogger("QUICKACCESS")
    connection.send({"key": "HideCommandPrompt"})
    logger.debug(f"{TRIGGER_HOTKEY} was released!")
    return True     

def listenKeyboard(connection: PipeConnection):
    return 
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))
    logger = logging.getLogger("QUICKACCESS")
    logger.debug(f"Start listening keyboard")
    if 1:
        keyboard.add_hotkey(TRIGGER_HOTKEY, onTriggerPress, args=(connection,), suppress=True, trigger_on_release=False)
        keyboard.add_hotkey(TRIGGER_HOTKEY, onTriggerRelease, args=(connection,), suppress=True, trigger_on_release=True)
        keyboard.add_hotkey(QUIT_HOTKEY, onQuit, args=(connection,), suppress=True)
    
    while True:
        # Wait for the next event. We will get any of the keyboard events. Our registered callbacks
        # will be called before read_event() returns
        event = keyboard.read_event(suppress=False)
        # connection.send({"key": "ProcessKey", "data": event})
        

if __name__ == "__main__":
    pass 
