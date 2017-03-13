import wx
import win32gui as gui
import win32con as con
import win32clipboard as clipboard

import SendKeys

#=============================================================================
#===
#=============================================================================

class DefaultApplication(object):
    #---
    def __getSelectedText(self):
        clipboard.OpenClipboard()
        newData = ''
        newFormat = 0
        newFormat = clipboard.EnumClipboardFormats(newFormat)
        print newFormat        
        if 1 or newFormat == con.CF_UNICODETEXT or newFormat == con.CF_TEXT:
            print 'gettting data'
            newData = clipboard.GetClipboardData(newFormat)
        clipboard.CloseClipboard()
        print 'cv: ' 
        print newData
        return newData
    def __getSelectedTextWX(self):
        text = ''
        SendKeys.SendKeys('^c')
        if wx.TheClipboard.Open():
            if wx.TheClipboard.IsSupported(wx.DataFormat(wx.DF_TEXT)):
                data = wx.TextDataObject()
                wx.TheClipboard.GetData(data)
                text = data.GetText()
            wx.TheClipboard.Close()
        return text
    def __setSelectedTextWX(self, text):
        if wx.TheClipboard.Open():
            data = wx.TextDataObject(text)
            wx.TheClipboard.SetData(data)
            wx.TheClipboard.Close()
        SendKeys.SendKeys('^v')
    
    selectedText = property(__getSelectedTextWX, __setSelectedTextWX)
    
    #---
    def __getTitle(self):
        return gui.GetWindowText(self.hwnd)
    title = property(__getTitle)
    
    #---
    def __getWindows(self):
        return []
    windows = property(__getWindows)
    
    #---
    def __getWindowClass(self):
        return gui.GetClassName(self.hwnd)
    windowClass = property(__getWindowClass)
        
    #---
    def __init__(self, hwnd = None):
        '''
        If hwnd is None, current window will be retrieved
        '''
        object.__init__(self)
        
        if hwnd:
            self.hwnd = hwnd
        else:
            self.hwnd = win32gui.GetActiveWindow()
        
        
    #---
    def dump(self):
        print 'hwnd         : %d' % self.hwnd
        print 'title        : %s' % self.title
        print 'selected text: %s' % self.selectedText
    
    
        
        

#=============================================================================
#===
#=============================================================================
if __name__ == '__main__':
    print 'defaultapplication.py'
    
    app = DefaultApplication()
    print app.title
    print app.selectedText
    
    