
#standard
import win32com as com
import win32com.client
import win32gui as gui

#internal
from defaultapplication import DefaultApplication

#=============================================================================
#===
#=============================================================================
class MSIE(DefaultApplication):
    def __init__(self, hwnd = None):
        self.ie = None
        windows = com.client.Dispatch('{9BA05972-F6A8-11CF-A442-00A0C90A8F39}')
        for i in range(1, windows.Count):
            wndText = gui.GetWindowText(int(windows[i].HWND))
            if 1:
                print i
                print windows[i].HWND
                print wndText
            if windows[i].HWND == hwnd:
                self.ie = windows[i]
                break
        
        if not self.ie:
            #Not found for some reason or the hwnd was not given:
            #we create a new instance
            self.ie = com.client.Dispatch('InternetExplorer.Application')
            self.ie.Visible = True
            
            