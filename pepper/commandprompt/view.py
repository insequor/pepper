"""
"""
# Standard Imports
import logging
from multiprocessing import Process
from multiprocessing.connection import PipeConnection
import os
from pathlib import Path
import random
import time

# Third Party Imports 
import webview

# Internal Imports



class Api:
    window: webview.Window 

    def __init__(self):
        self.__visible = False 
        self.__hideWhenRequested = False 
        self.__ignoreShowHideRequest = False 
        self.__logger = logging.getLogger("COMMANDPROMPT")

    def _showRequested(self):
        if self.__ignoreShowHideRequest:
            return 
        
        if not self.__visible:
            self._show() 
        else:
            # If we are already visible and receive this command 
            # It means we want it to be in auto-hide mode
            self.__hideWhenRequested = True 
            

    def _hideRequested(self):
        if self.__ignoreShowHideRequest:
            return 
        
        if self.__hideWhenRequested:
            self.execute()
        else:
            self.__ignoreShowHideRequest = True 
         
    def _show(self):
        self.window.show()
        # NOTE: Something is broken, window.hidden is not reliable
        self.__visible = True 
        self.__hideWhenRequested = False  # We need the second show request to switch to sticky auto-hide mode
        self.__ignoreShowHideRequest = False

    def _hide(self):
        self.window.hide()
        # NOTE: Something is broken, window.hidden is not reliable
        self.__visible = False 
        self.__hideWhenRequested = False 
        self.__ignoreShowHideRequest = False 

    def execute(self):
        self.__logger.debug("EXECUTE COMMAND")
        self._hide()
        response = {
            'message': 'Execute Command'
        }
        return response
    
    def cancel(self):
        self._hide()
        response = {
            'message': 'Cancel'
        }
        return response


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

    with open(Path(__file__).parent / "commands.html", "r") as file:
        html = file.read()

    api = Api()
    window = webview.create_window('API example', html=html, js_api=api)
    api.window = window 
    window.events.closed += onClosed
    
    
    def startCallback(connection: PipeConnection, window: webview.Window):
        """This method is called by the webview.start as art of the thread
        
            This function is executed in a new thread 
        """
        window.hide()
        
        # NOTE: Alternatively we can use this thread to listen the keyboard events instead 
        # of using a dedicated process for listenKeyboard function. It gives us an additional 
        # benefit that both key handling and the view are in the same process. But I am keeping
        # it as it is for now since different processes force us to define a cleaner interaction
        # betweent them

        showMessageIsReceived = False 
        hideOnHideMessage = False 
        while True:
            msg = connection.recv()
            match msg:
                case "ShowCommandPrompt":
                    api._showRequested()
                case "HideCommandPrompt":
                    api._hideRequested()
                case "exit":
                    window.destroy()
                    return
    
    webview.start(func=startCallback, args=(connection, window))


if __name__ == "__main__":
    pass 
