#=============================================================================
#=== Ozgur Aydin Yuksel, 2007 (c)
#=============================================================================

# Standard Imports
import ctypes
import logging 

# Thirdparty Imports

# Internal Imports
from pepper import ui 

__doc__  = '''
    Applications package to deal with the wrapping of different applications
'''


#Currently active application
current = None

#
#
#
def getOutlookApp():
    from msoutlook import MSOutlook  # type: ignore
    return MSOutlook()


def getOneNoteApp():
    from msonenote import MSOneNote  # type: ignore
    return MSOneNote()


#
#
#
def setCurrent(hwnd = None):
    global current
    if hwnd is None:
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        
    wndText = ui.getWindowText(hwnd)
    wndClass = ui.getWindowClassName(hwnd)
        
    logging.debug(f"DefaultApplication")
    logging.debug(f"   hwnd: {hwnd}")
    logging.debug(f"   wndClass: {wndClass}")
    logging.debug(f"   wndText: {wndText}")
        
    if 0 and wndClass == 'wndclass_desked_gsk' and wndText.find('Microsoft Visual C++'):
        from msvisualstudio import MSVisualStudio
        current = MSVisualStudio(hwnd)
    elif 0 and wndClass == 'OpusApp' and wndText.find('Microsoft Word'):
        from msword import MSWord
        current = MSWord(hwnd)
    elif wndClass == 'rctrl_renwnd32':
        from msoutlook import MSOutlook
        current = MSOutlook(hwnd)
    elif wndClass == 'Framework::CFrame':
        from msonenote import MSOneNote
        current = MSOneNote(hwnd)
    else:
        from .defaultapplication import DefaultApplication
        current = DefaultApplication(hwnd)
        
#=============================================================================
if __name__ == '__main__':
    print('applications.__init__.py')