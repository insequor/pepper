"""
"""
# Standard Imports
import logging
import multiprocessing
from multiprocessing.connection import PipeConnection
import os 

# Third Party Imports
from fastapi import FastAPI
from uvicorn import Config, Server
from nicegui import ui

# Internal Imports

class App:

    def start(self, connectionToSend: PipeConnection):
        """ Start the application """
        logger = logging.getLogger("WEBSERVER")
        logger.setLevel(os.environ.get("LOGLEVEL", "DEBUG"))
        logger.info("START")

        server_ip = "127.0.0.1"
        server_port = 8080 
        config = Config(f"{__name__}:app", host=server_ip, port=server_port, log_level="debug")
        instance = UvicornServer(config=config)
        instance.start()
        self.server = instance 

    def stop(self):
        """ Stop the application """
        logger = logging.getLogger("WEBSERVER")
        logger.debug("Stop requested, ending the application")
        self.server.stop()
        

class UvicornServer(multiprocessing.Process):

    def __init__(self, config: Config):
        super().__init__()
        self.server = Server(config=config)
        self.config = config

    def stop(self):
        self.terminate()

    def run(self, *args, **kwargs):
        self.server.run()

    
app = FastAPI()


@app.get('/')
def read_root():
    return {'Hello': 'World'}


@ui.page('/show')
def show():
    ui.image('https://picsum.photos/id/377/640/360')


ui.run_with(app)


def main():
    logger = logging.getLogger("WEBSERVER")
    logger.setLevel(os.environ.get("LOGLEVEL", "DEBUG"))
    logger.info("START")

    server_ip = "127.0.0.1"
    server_port = 8080 
    config = Config(f"{__name__}:app", host=server_ip, port=server_port, log_level="debug")
    instance = UvicornServer(config=config)
    instance.start()
    instance.run()
    instance.stop()
    logger.info("END")

if __name__ == "__main__":
    pass 
