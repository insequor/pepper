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

TRIGGER_HOTKEY = "capslock"
# NOTE: We should not need quit hotkey, we will use the app icon tro handle this
# or have an exit command in the application
QUIT_HOTKEY = "ctrl+e"

class App:
    def start(self, connectionToSend: PipeConnection):
        """ We start both the keyboard listener and the webview applications """
        logger = logging.getLogger("COMMANDPROMPT")
        logger.setLevel(os.environ.get("LOGLEVEL", "DEBUG"))
        logger.info("START")
        webView = Process(target=startWebView, args=(connectionToSend, f'http://localhost:8080/show', self), daemon=True)
        webView.start()

    def stop(self):
        """ Stop the application """
        logger = logging.getLogger("COMMANDPROMPT")
        logger.info("Stop Requested Ending the application")


def startWebView(connection: PipeConnection, urlToLoad: str, app: App):
    logging.basicConfig(level="DEBUG")
    logger = logging.getLogger("COMMANDPROMPT")
    logger.debug(f"Start web view for app {app}")
    
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
