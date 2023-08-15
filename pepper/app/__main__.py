"""
"""
# Standard Imports
import logging
import multiprocessing
import os

# Third Party Imports 

# Internal Imports
from pepper import commandprompt as cp
from pepper import webserver as ws
from pepper.app import App 


def main():
    logger = logging.getLogger("PEPPER")
    logger.setLevel(os.environ.get("LOGLEVEL", "DEBUG"))
    logger.info("START")

    connection, childConnection = multiprocessing.Pipe()
    apps: list[App] = [
        ws.App(),
        cp.App()
    ]

    for app in apps:
        app.start(childConnection)

    # Here we loop till we recive the close request
    msg = ''
    while 'exit' not in msg:
        msg = connection.recv()
        # logger.debug(f"    Received: {msg}")
        # for app in apps:
        #    app.onMessage(msg)
        # Send the received message to all children
        connection.send(msg)

    logger.debug("close request is received, we are ending the application")

    # We already send the exit message in above loop. Normally the apps should be listening and honoring 
    # that request. This is for the cases where they do not listen the connections
    for app in apps:
        app.stop()

    logger.info("END")
    

if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    main()
