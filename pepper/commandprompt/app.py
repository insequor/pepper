"""
"""
# Standard Imports
import logging
from multiprocessing import Process
from multiprocessing.connection import PipeConnection
import os

# Third Party Imports 

# Internal Imports
from .quickaccess import listenKeyboard
from .view import startWebView

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


if __name__ == "__main__":
    pass 
