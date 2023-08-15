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


def onQuit(connection: PipeConnection):
    logger = logging.getLogger("QUICKACCESS")
    logger.debug("Quit hotkey is pressed, sending the request to exit the application")
    connection.send("exit")
    

def onTriggerPress(connection: PipeConnection):
    logger = logging.getLogger("QUICKACCESS")
    if App.active:
        return 
    App.active = True
    connection.send("ShowCommandPrompt")
    logger.debug(f"{TRIGGER_HOTKEY} was pressed!")
    

def onTriggerRelease(connection: PipeConnection):
    logger = logging.getLogger("QUICKACCESS")
    if not App.active:
        return 
    App.active = False
    connection.send("HideCommandPrompt")
    logger.debug(f"{TRIGGER_HOTKEY} was released!")
    

def listenKeyboard(connection: PipeConnection):
    logging.basicConfig(level="DEBUG")
    logger = logging.getLogger("QUICKACCESS")
    logger.debug(f"Start listening keyboard")
    keyboard.add_hotkey(TRIGGER_HOTKEY, onTriggerPress, args=(connection,), suppress=True, trigger_on_release=False)
    keyboard.add_hotkey(TRIGGER_HOTKEY, onTriggerRelease, args=(connection,), suppress=True, trigger_on_release=True)
    keyboard.add_hotkey(QUIT_HOTKEY, onQuit, args=(connection,), suppress=True)
    while not App.stopRequested:
        # Wait for the next event.
        _ = keyboard.read_event()
    logger.debug("Keyboard event loop is ended")


class App:
    stopRequested: bool = False
    active: bool = False 

    def start(self, connection: PipeConnection):
        """ We start both the keyboard listener and the webview applications """
        logger = logging.getLogger("COMMANDPROMPT")
        logger.setLevel(os.environ.get("LOGLEVEL", "DEBUG"))
        logger.info("START")
        self.processes = [
            Process(target=listenKeyboard, args=(connection,), daemon=True), 
            Process(target=startWebView, args=(connection, f'http://localhost:8080/show'), daemon=True)
        ]
        for process in self.processes:
            process.start()

    def stop(self):
        """ Stop the application """
        logger = logging.getLogger("COMMANDPROMPT")
        logger.info("Stop Requested Ending the application")
        # Each process also receives the exit message
        for process in self.processes:
            process.kill()


def startWebView(connection: PipeConnection, urlToLoad: str):
    logging.basicConfig(level="DEBUG")
    logger = logging.getLogger("COMMANDPROMPT")
    logger.debug(f"Start web view")
    
    def onClosed():
        logger.debug("Window is closed, requesting to end the application")
        try:
            connection.send('exit')
        except Exception:
            pass  # If the pipe is already closed we do not care

    window = webview.create_window('Pepper', url=urlToLoad)
    window.events.closed += onClosed
    
    def startCallback(connection: PipeConnection, window: webview.Window):
        """This method is called by the webview.start as art of the thread
        
            This function is executed in a new thread 
        """
        window.hide()
        while True:
            msg = connection.recv()
            logger.debug(f"    Received: {msg}")
            match msg:
                case "ShowCommandPrompt":
                    window.show()
                case "HideCommandPrompt":
                    window.hide()
                case "exit":
                    window.destroy()
                    return
    
    webview.start(func=startCallback, args=(connection, window))
    

def main():
    pass


if __name__ == "__main__":
    pass 
