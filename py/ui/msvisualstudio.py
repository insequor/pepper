import wx
import win32gui as gui
import win32con as con
import win32com as com
import win32com.client
import win32process as process
import pythoncom

import win32clipboard as clipboard

import SendKeys

from defaultapplication import DefaultApplication

#=============================================================================
#===
#=============================================================================

class MSVisualStudio(DefaultApplication):
    #---
    def __getSelectedText(self):
        assert(self.dte)
        if self.dte.ActiveDocument:
            return str(self.dte.ActiveDocument.Selection)
        return ''
    
    #---
    def __setSelectedText(self, text):
        assert(self.dte)
        if self.dte.ActiveDocument:
            self.dte.ActiveDocument.Selection = text
    selectedText = property(__getSelectedText, __setSelectedText)
    
    #---
    def __getWindows(self):
        assert(self.dte)
        return self.dte.Windows
    windows = property(__getWindows)
    
    #---
    def __init__(self, hwnd = None):
        '''
        If hwnd is None, current window will be retrieved
        '''
        DefaultApplication.__init__(self, hwnd)
        if hwnd:
            pids = process.GetWindowThreadProcessId(hwnd)
        else:
            pids = None
        
        self.dte = None    
        ctx = pythoncom.CreateBindCtx()
        rot = pythoncom.GetRunningObjectTable()
        for mk in rot:
            name = mk.GetDisplayName(ctx, None)
            if name.find('VisualStudio.DTE') < 0:
                continue
                
            if not pids:
                obj = rot.GetObject(mk)
                interface = obj.QueryInterface (pythoncom.IID_IDispatch)
                self.dte = com.client.Dispatch (interface)
                break
                
            pos = name.rfind(':')
            if pos < 0:
                continue
            name = name[pos + 1:]
            val = int(name)
            if val in pids:
                obj = rot.GetObject(mk)
                interface = obj.QueryInterface (pythoncom.IID_IDispatch)
                self.dte = com.client.Dispatch (interface)
                break
                
    #---
    def getWindowTitle(self, wnd):
        assert(wnd)
        return str(wnd)
        
    #---
    def getWindowPath(self, wnd):
        assert(wnd)
        return wnd.Document.FullName
        
    #---
    def showWindow(self, wnd):
        assert(wnd)
        wnd.Visible = True    
        

#=============================================================================
#===
#=============================================================================
if __name__ == '__main__':
    print 'msvisualstudio.py'
    
    app = MSVisualStudio()
    print app.title
    print app.selectedText
    
    