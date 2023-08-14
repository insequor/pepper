"""
    This is copied from https://gist.github.com/eli-kha/06a47bfdf1e50f4cdfc3f43a199a6d2d
    And added some sample code for the keyboard. This version handles the following processes:
    * Main process to manage the servers
    * UvicornServer to serve the webserver
    * Child process to open the webview 
    * Child process to listen the keyboard
"""

#!/usr/bin/env python3
import logging
import multiprocessing
import tempfile

from fastapi import FastAPI
from uvicorn import Config, Server
import webview
import keyboard 
from nicegui import ui

LEVEL = "DEBUG"

TRIGGER_HOTKEY = "capslock"
# NOTE: We should not need quit hotkey, we will use the app icon tro handle this
# or have an exit command in the application
QUIT_HOTKEY = "ctrl+e"

class App:
    stop: bool = False
    active: bool = False

def onQuit(logger):
    def cb():
        logger.debug("quit")
        App.stop = True 
    return cb 

def onTriggerPress(logger):
    def cb():
        if App.active:
            return 
        App.active = True
        logger.debug(f"{TRIGGER_HOTKEY} was pressed!")
    return cb

def onTriggerRelease(logger):
    def cb():
        if not App.active:
            return 
        App.active = False
        logger.debug(f"{TRIGGER_HOTKEY} was released!")
    return cb 

def start_keyboard(pipe_send):
    logger = logging.getLogger("KEYBOARD")
    logger.setLevel(LEVEL)
    logger.info("START KEYBOARD APP")

    keyboard.add_hotkey(TRIGGER_HOTKEY, onTriggerPress(logger), suppress=True, trigger_on_release=False)
    keyboard.add_hotkey(TRIGGER_HOTKEY, onTriggerRelease(logger), suppress=True, trigger_on_release=True)
    keyboard.add_hotkey(QUIT_HOTKEY, onQuit(logger), suppress=True)
    while not App.stop:
        # Wait for the next event.
        _ = keyboard.read_event()
        logger.info(f'READ EVENT App.stop = {App.stop}')
    logger.debug("KEYBOARD: Application is stopped")
    print("KEYBOARD: Application is stopped")
    try:
        pipe_send.send('closed')
    except Exception:
        pass  # If the pipe is already closed we do not care


class UvicornServer(multiprocessing.Process):

    def __init__(self, config: Config):
        super().__init__()
        self.server = Server(config=config)
        self.config = config

    def stop(self):
        self.terminate()

    def run(self, *args, **kwargs):
        self.server.run()


def start_window(pipe_send, url_to_load):
    logger = logging.getLogger("WINDOW")
    logger.setLevel(LEVEL)
    logger.info("START WINDOW APP")

    def on_closed():
        logger.debug("WINDOW: Application is stopped")
        print("WINDOW: Application is stopped")
        try:
            pipe_send.send('closed')
        except Exception:
            pass  # If the pipe is already closed we do not care

    win = webview.create_window('Demo', url=url_to_load)
    win.events.closed += on_closed
    webview.start(storage_path=tempfile.mkdtemp())
    
    
app = FastAPI()


@app.get('/')
def read_root():
    return {'Hello': 'World'}


@ui.page('/show')
def show():
    ui.image('https://picsum.photos/id/377/640/360')


ui.run_with(app)


def main():
    # logging.basicConfig(level="DEBUG")
    logger = logging.getLogger("PEPPER")
    logger.setLevel(LEVEL)
    logger.info("START MAIN APP")

    server_ip = "127.0.0.1"
    server_port = 8080
    conn_recv, conn_send = multiprocessing.Pipe()
    windowsp = multiprocessing.Process(target=start_window, args=(conn_send, f'http://{server_ip}:{server_port}/show'), daemon=True)
    windowsp.start()

    keyboardsp = multiprocessing.Process(target=start_keyboard, args=(conn_send, ), daemon=True)
    keyboardsp.start()

    config = Config("__main__:app", host=server_ip, port=server_port, log_level="debug")
    instance = UvicornServer(config=config)
    instance.start()

    window_status = ''
    while 'closed' not in window_status:
        # get a unit of work
        window_status = conn_recv.recv()
        # report
    
    logger.info(f'got {window_status}')
    App.stop = True
    logger.info(f'App.stop = {App.stop}')
    instance.stop()


if __name__ == '__main__':
    main()
    