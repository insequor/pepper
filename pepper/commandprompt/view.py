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
import webview.platforms.winforms
from pywinauto.controls.hwndwrapper import HwndWrapper


# Internal Imports
from pepper.commandprompt import commander 
from pepper.commandprompt.controller import ControllerHandler, Controller
from pepper import applications

class Api:
    window: webview.Window 

    def __init__(self):
        self.__visible = False 
        self.__hideWhenRequested = False 
        self.__ignoreShowHideRequest = False 
        self.__logger = logging.getLogger("COMMANDPROMPT")
        commander.Manager.commandsFolder = Path("pepper", "commands")
        self.commander = commander.Manager()
        self.commander.refresh()
        # TODO: 
        _ = self.commander.getOptions()

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
            self.execute("N/A", "N/A")
        else:
            self.__ignoreShowHideRequest = True 
         
    def _show(self):
        applications.setCurrent(None)
        
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

    def execute(self, value: str, selection: str):
        self.__logger.debug(f"EXECUTE COMMAND: '{value}' '{selection}'")
        self.commander.command = selection 
        self.commander.command.execute(selection, "")
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

class WebViewControllerHandler(ControllerHandler):
    
    def __init__(self, window: webview.Window):
        self.window = window 
    
    def onControllerMessage(self, msg):
        match msg:
            case ControllerHandler.activated:
                self.window.show()
                self.window.on_top = True 
                logging.debug(f"WINDOW GUI {self.window.gui} ({type(self.window.gui)})")
            case ControllerHandler.deactivated:
                self.window.hide()
            case _:
                logging.debug(f"WebViewControllerHandler.onControllerMessage({msg})")
        
    def onTextChanged(self, text, lastEntry):
        logging.debug(f"CH.onTextChanged({text}, {lastEntry})")
        
    def onOptionsChanged(self, options):
        logging.debug(f"CH.onOptionsChanged({options})")
        
    def onOptionSelectionChanged(self, options, selection):
        logging.debug(f"CH.onOptionSelectionChanged({options}, {selection})")
        

# TODO: Fix this, we keep it so objects do not die
class Data:
    controller: Controller 
    controllerHandler: ControllerHandler


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

    # TODO: When we show the UI we should make sure that it has the focus
    # Otherwise key events are still send to the old window. This way we do not 
    # need to suppress the key events
    with open(Path(__file__).parent / "commands.html", "r") as file:
        html = file.read()

    url = "http://localhost:8080/test/commandprompt"
    api = Api()
    # window = webview.create_window('API example', url=url, js_api=api, hidden=True)
    window = webview.create_window('API example', html=html, hidden=True)
    Data.controllerHandler = WebViewControllerHandler(window)
    Data.controller = Controller(Data.controllerHandler)

    api.window = window 
    window.events.closed += onClosed
    
    def startCallback(connection: PipeConnection, window: webview.Window):
        """This method is called by the webview.start as art of the thread
        
            This function is executed in a new thread 
        """
        # NOTE: Alternatively we can use this thread to listen the keyboard events instead 
        # of using a dedicated process for listenKeyboard function. It gives us an additional 
        # benefit that both key handling and the view are in the same process. But I am keeping
        # it as it is for now since different processes force us to define a cleaner interaction
        # betweent them

        while True:
            msg = connection.recv()
            match msg["key"]:
                case "ShowCommandPrompt":
                    api._showRequested()
                case "HideCommandPrompt":
                    api._hideRequested()
                case "exit":
                    window.destroy()
                    return
                case "ProcessKey":
                    Data.controller.processKey(msg["data"])


    webview.start(func=startCallback, args=(connection, window), debug=False)


if __name__ == "__main__":
    pass 
