""" 
    Development script which is executed by the script command 

"""

# Standard Imports
import logging 
import os 
from xml.etree import ElementTree
# Third Party Imports
import pywinauto as pwa 
from pywinauto.application import Application
from win32com import client 

# Internal Imports 
from pepper import applications 
from pepper.applications.msonenote import MSOneNote, app as one


def i_(level=0):
    return " " * 4 * level


def getSelectionFromOneNote():
    logging.debug("getSelectionFromOneNote()")
    currentApp = applications.current
    assert isinstance(currentApp, MSOneNote)
    logging.debug(f"{i_(2)}Selected Text: {currentApp.selectedText}")
    """
        Ctrl+C is not really reliable. Maybe it is best that we leave it to the user 
        It is good to check why Ctrl+C does not work but it is more important with Ctrl+V
        For Ctrl+C we say the user copies to clipboard
        In worst case we can say the user does the Ctrl+V as well
    """
    return 
    # Slection enum 2
    # Page API is here: https://learn.microsoft.com/en-us/office/client-developer/onenote/window-interfaces-onenote
    logging.debug(f"{i_(1)}Windows.Count: {one.Windows.Count}")
    logging.debug(f"{i_(1)}Windows.CurrentWindow: {one.Windows.CurrentWindow}")
    logging.debug(f"{i_(1)}Windows.CurrentWindow.CurrentPageId: {one.Windows.CurrentWindow.CurrentPageId}")
    logging.debug(f"{i_(1)}Windows.CurrentWindow.DockedLocation: {one.Windows.CurrentWindow.DockedLocation}")
    pageHierarchy = one.GetPageContent(one.Windows.CurrentWindow.CurrentPageId, pageInfoToExport=client.constants.piAll)
    pageTree = ElementTree.fromstring(pageHierarchy)
    logging.debug(pageTree)
    ElementTree.indent(pageTree)
    print(ElementTree.tostring(pageTree, encoding="unicode"))

    # logging.debug(f"{i_(1)}Windows: {one.Window}")
    # logging.debug(f"{i_(1)}Count: {one.Count}")    
    # logging.debug(f"{i_(1)}Name: {one.Name}")
    

def checkWhatWeCanGetFromCurrentApplication():
    logging.debug("checkWhatWeCanGetFromCurrentApplication()")
    # applications.setCurrent()
    currentApp = applications.current
    logging.debug(f"{i_(1)}Current Application: {currentApp}")
    if currentApp is not None:
        logging.debug(f"{i_(2)}Title: {currentApp.title}")
        logging.debug(f"{i_(2)}Handle: {currentApp.hwnd}")
        logging.debug(f"{i_(2)}Selected Text: {currentApp.selectedText}")
        app = Application().connect(handle=currentApp.hwnd,  timeout=10)
        logging.debug(f"{i_(2)}pws App: {app}")
        logging.debug(f"{i_(3)}Top Window: {app.top_window()}")
        # below call gives unicode error
        # app.top_window().dump_tree(filename='topwindow.txt')
        logging.debug(f"{i_(3)}Windows: ")
        """ 
            Visual Studio Code:
                Windows list the active code editors from each visual studio code instances that are active 

            Remnote:

        """
        for wnd in app.windows():
            logging.debug(f"{i_(4)}{wnd}")
            
    else:
        logging.debug("Nothing more to say")

def main():
    logging.debug("Script Test") 
    # checkWhatWeCanGetFromCurrentApplication()
    getSelectionFromOneNote()

if __name__ == "__main__":
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"))
    main()
