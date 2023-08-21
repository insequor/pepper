"""
"""
# Internal Imports
import logging 

# Third Party Imports
from pynput import keyboard 
import win32con


class KeyboardListener(keyboard.Listener):
    def __init__(self):
        
        def onPress(key):
            return self.onPress(key)
        
        def onRelease(key):
            return self.onRelease(key)
        
        def win32EventFilter(msg, data):
            return self.win32EventFilter(msg, data)
        
        super().__init__(
            on_press=onPress,
            on_release=onRelease,  # type: ignore
            win32_event_filter=win32EventFilter,
            suppress=False
        ) 

    def onPress(self, key):
        """ Return True if you want to exit listening """
        logging.debug(f"   onPress({key})")
            
    def onRelease(self, key):
        """ Return False if you want to exit listening """
        logging.debug(f"    onRelease({key})")
        if key == keyboard.Key.esc:
            return False 

    def win32EventFilter(self, msg=None, data=None):
        """ Return True if you want to process the event, otherwise False """
        logging.debug(f"win32EventFilter({msg}, {data})")
        for attr in dir(data):
            if not attr.startswith("__"):
                logging.debug(f"    {attr}: {getattr(data, attr)}")

        logging.debug(f"KeyID={data.vkCode}, Ascii={self._event_to_key(msg, data.vkCode)}")

        match msg:
            case 256:
                logging.debug("     Key Press Event")
            case 257:
                logging.debug("     Key Release Event")
            case _:
                logging.debug(f"    Unknown event: {msg}")
        
        if data.vkCode == win32con.VK_CAPITAL:
            self.suppress_event()  # It looks like this method is only available for win32
        if data.vkCode == win32con.VK_ESCAPE:
            logging.debug("Supposed to exit here")
            self.stop()
    

def main():
    logging.debug("Start")
    with KeyboardListener() as listener:
        logging.debug("Before Join")
        listener.join()
        logging.debug("After Join")


if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    
    main()
