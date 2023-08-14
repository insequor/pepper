"""
    Sample app to see how we can use webview as a frontend

    Things to check:
    [+] Can I provide content dynamically or should it always be a URL
        We can pass a URL, html or directly a server app like Flask application instance 
    
    [+] Can I register my hook up so I know when I can get into python
        There is an example To Do application. We can provide an Api class with the methods 
        to be exposed to the web frontent. This way we can fall back to our own application

        This (https://pywebview.flowrl.com/examples/js_api.html) is an example where the HTML
        UI communicates with the application via js_api. This one does not require a web server 
        run. It looks neat. 

        This (https://pywebview.flowrl.com/guide/interdomain.html) explains the two options to expose 
        python methods to javascript

    [?] Can I run my own event loop? 
        I could not find an answer for that but I can define a callback which will be executed 
        in a new thread by the main application. Within this thread I can communicate with the 
        keyboard package to handle the key events

    [ ] Can I use it with FastAPI in case if I want to run a local web-server
        There is direct support for Flask. And using the js_api we do not need a web server, but let's 
        assume we wanted to write a web app and wanted to use this one as UI. Here 
        (https://gist.github.com/eli-kha/06a47bfdf1e50f4cdfc3f43a199a6d2d) is an example to use with FastAPI.
        It uses NiceGUI (https://nicegui.io/) for the UI elements in the HTML page directly 
        
        This example also uses multiprocess (https://docs.python.org/3/library/multiprocessing.html) package 
        to create window and server in different processes rather than threads. It might be a good example
        to use keyboard and view in different processes
"""
# Standard Imports
import logging 

# Third Party Imports
import webview
import keyboard 

# Internal Imports


TRIGGER_HOTKEY = "capslock"
# NOTE: We should not need quit hotkey, we will use the app icon tro handle this
# or have an exit command in the application
QUIT_HOTKEY = "ctrl+e"

class App:
    stop: bool = False
    active: bool = False

def onQuit():
    logging.debug("quit")
    App.stop = True 
    
def onTriggerPress():
    if App.active:
        return 
    App.active = True
    logging.debug(f"{TRIGGER_HOTKEY} was pressed!")


def onTriggerRelease():
    if not App.active:
        return 
    App.active = False
    logging.debug(f"{TRIGGER_HOTKEY} was released!")


def main():
    html = """
        <html>
            <body style="background-color:rgba(255, 0, 0, 0.5);opacity:0.5">
                <h1>Hi There!</h1>
            </body>
        </html>
    """
    window = webview.create_window(
        title='Hello world', 
        url='https://pywebview.flowrl.com/',
        html=html,
        fullscreen=False,
        frameless=False,
        on_top=True,
        transparent=True
    )
    
    logging.info("Starting event loop")
    def startCallback(window):
        """This method is called by the webview.start as art of the thread
        
            This function is executed in a new thread so we do not need to exit 
            it.
        """
        keyboard.add_hotkey(TRIGGER_HOTKEY, onTriggerPress, suppress=True, trigger_on_release=False)
        keyboard.add_hotkey(TRIGGER_HOTKEY, onTriggerRelease, suppress=True, trigger_on_release=True)
        keyboard.add_hotkey(QUIT_HOTKEY, onQuit, suppress=True)
        while not App.stop:
            # Wait for the next event.
            event = keyboard.read_event()
        logging.info("Application is stopped")
        window.destroy()

    webview.start(func=startCallback, args=(window,), debug=True)

    logging.info("Exiting application")
    App.stop = True 
    

if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    main()
