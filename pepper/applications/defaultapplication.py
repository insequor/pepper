
# Standard Imports
import logging 

# Thirparty Imports
import keyboard
import win32gui as gui
import win32con as con
import win32clipboard as clipboard

# Internal Imports
from pepper import ui 

#=============================================================================
#===
#=============================================================================

class DefaultApplication:
    @property 
    def selectedText(self) -> str | None:
        keyboard.send("ctrl+c")
        return ui.getClipboardText()
        
    @selectedText.setter
    def selectedText(self, text):
        ui.putInClipboard(text)
        logging.debug(f"Default application sending ctrl + v for text: {text}")
        keyboard.send("ctrl+v")
    
    @property
    def title(self):
        return gui.GetWindowText(self.hwnd)
    
    @property 
    def windows(self):
        return []
    
    @property
    def windowClass(self):
        return gui.GetClassName(self.hwnd)
        
    #---
    def __init__(self, hwnd: int):
        self.hwnd = hwnd
                
    #---
    def dump(self):
        logging.info("hwnd         : {self.hwnd}")
        logging.info("title        : {self.title}")
        logging.info("selected text: {self.selectedText}")


if __name__ == '__main__':
    pass 
    