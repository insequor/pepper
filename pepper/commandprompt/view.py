"""
"""
# Standard Imports
import logging
from multiprocessing import Process
from multiprocessing.connection import PipeConnection
import os

# Third Party Imports 
import webview

# Internal Imports


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


if __name__ == "__main__":
    pass 
