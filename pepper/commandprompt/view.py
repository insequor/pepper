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
from pywinauto.findwindows    import find_window
from pywinauto.win32functions import BringWindowToTop

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
        commander.Manager.commandsFolder = Path(".", "pepper", "commands")
        self.commander = commander.Manager()
        self.__logger.debug(f"COMMAND Object is {self.commander}")
        self.commander.refresh()
        # TODO: 
        options = self.commander.getOptions()
        self.__logger.debug(f"OPTIONS: {options}")
        self.__logger.debug(f"({self})")

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
        Data.controller.activate(None, None)

        def callback(result):
            print(f"===== CALLBACK: {result}")

        self.window.evaluate_js(
            """
            new Promise((resolve, reject) => {
                setTimeout(() => {
                    console.log('Whaddup!');
                    onShowWindow();
                }, 100);
            });
            """, callback)
            
    def _hide(self):
        self.window.hide()
        # NOTE: Something is broken, window.hidden is not reliable
        self.__visible = False 
        self.__hideWhenRequested = False 
        self.__ignoreShowHideRequest = False 

    def getAllOptions(self):
        self.__logger.debug(f"Get All Options: {self.commander} ({self})")
        self.commander.refresh()
        options = self.commander.getOptions() 
        self.__logger.debug(f"OPTIONS: {options}")
        self.__logger.debug(f"CURRENT COMMAND: {self.commander.command}")
        response = {
            'message': 'Get All Options',
            "options": options
        }
        return response
    
    def execute(self, value: str, selection: str):
        self.__logger.debug(f"EXECUTE COMMAND: '{value}' '{selection}'")
        self.__logger.debug(f"COMMAND Object is {self.commander}")
        self.commander.command = selection 
        Data.controller.execute(selection, None)
        # self.commander.command.execute(selection, "")
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
        self.__window = window 
        self.__title = "Pepper"
        self.__lastEntry = ""
        self.__commandLine = ""
        self.__listLines = []
        self.__selectedIdx = -1
        self.__startIdx = -1 
    
    def onControllerMessage(self, msg):
        try:
            self.__commandLine = ""
            self.__lastEntry = ""
            match msg:
                case ControllerHandler.activated:
                    self.__window.show()
                    if not self.__window.on_top:
                        self.__window.on_top = True
                    if 0:
                        
                        window = find_window(title="Pepper Quick Access")
                        BringWindowToTop(window)
                    self.loadHtml()
                case ControllerHandler.deactivated:
                    self.__window.hide()
                case _:
                    logging.debug(f"CH.onControllerMessage: ({msg})")
        except Exception: 
            logging.exception("... exception")
        finally:    
            pass
        
    def onTextChanged(self, command, option):
        if option:
            self.__commandLine = option
            self.__title = command + "..."
        else:
            self.__commandLine = command 
            self.__title = "Start Typing..."
        self.__lastEntry = self.__commandLine 
        self.loadHtml()

    def onOptionsChanged(self, options):
        self.__listLines = options 
        self.__startIdx = -1
        self.loadHtml()

    def onOptionSelectionChanged(self, options, selection):
        self.__selectedIdx = selection 
        self.loadHtml()

    def __replaceSelected(self, text, selected):
        '''
            This method can be improved using re module but currently works just fine
            It does sort of case insensitive replacement. Search is based on lower 
            characters. It preserves the original cases from found string while replacing
        '''
        start = text.lower().find(selected.lower())
        if (start == -1):
            return text
        end = start + len(selected)
        return text[:start] + '<font color=#0000FF>' + text[start:end] + '</font>' + text[end:]

    @property 
    def html(self) -> str:
        # Title first
        text = '<font size="+6">' + self.__title + '<hr><br>'
        
        # Then the user entry line
        if self.__commandLine != '':
            text += self.__commandLine
        else:
            text += '<br>'
        text +='</font>'
        
        #end the options
        replText = '<font color=#0000FF>' + self.__lastEntry + '</font>'
        start = self.__startIdx
        if self.__selectedIdx < start:
            start = self.__selectedIdx
        if start == -1:
            start = 0
        count = 9
        if self.__selectedIdx - start > count - 1:
            start = self.__selectedIdx - count + 1
        self.__startIdx = start
        end = start + count
        if end >= len(self.__listLines):
            end = len(self.__listLines)
         
        for idx in range(start, end):
            item = self.__listLines[idx].replace(' ', ' ')
            item = self.__replaceSelected(item, self.__lastEntry)
            if idx == self.__selectedIdx:
                item = '<font color=#00FF00>' + item + '</font>'
            text +=  '<br>' + item
        if end < len(self.__listLines) :
            text += '<br>...'
        return text 

    def loadHtml(self):
        self.__window.load_html(self.html)


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
            connection.send({"key": "exit"})
        except Exception:
            pass  # If the pipe is already closed we do not care

    # TODO: When we show the UI we should make sure that it has the focus
    # Otherwise key events are still send to the old window. This way we do not 
    # need to suppress the key events
    with open(Path(__file__).parent / "commands.html", "r") as file:
        html = file.read()

    window = webview.create_window("Pepper Quick Access", html="", hidden=False, on_top=True)
    Data.controllerHandler = WebViewControllerHandler(window)
    Data.controller = Controller(Data.controllerHandler)
    commander.manager.connection = connection
    window.events.closed += onClosed
    
    if Data.controller.keyboard is not None:
        logger.debug("--- Starting to listen the Keyboard")
        Data.controller.keyboard.start()
        Data.controller.keyboard.wait()

    def startCallback(connection: PipeConnection, window: webview.Window):
        """This method is called by the webview.start as art of the thread
        
            This function is executed in a new thread 
        """
        window.hide()

        while True:
            msg = connection.recv()
            logger.debug(f"    Received: {msg}")
            # for app in apps:
            #    app.onMessage(msg)
            # Send the received message to all children
            match msg["key"]:
                case "activate":
                    commandState, evt = msg["data"]
                    Data.controller.activate(commandState, evt)
                case "cancel":
                    Data.controller.cancel()
                case "execute":
                    complatedEntry, key = msg["data"]
                    Data.controller.execute(complatedEntry, key)

    webview.start(func=startCallback, args=(connection, window), debug=False)

    if Data.controller.keyboard:    
        Data.controller.keyboard.join()    
        logger.debug("--- Done listening to the Keyboard") 


if __name__ == "__main__":
    pass 
