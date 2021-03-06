#=============================================================================
#=== Ozgur Aydin Yuksel, 2007 (c)
#=============================================================================


__doc__ = \
"""
User interface components for Commander
"""
 
 
#standard
import os
import sys 
import getpass
import time


#third party
import win32gui as gui
import win32process
import win32con
import win32clipboard as clipboard
import pythoncom


#To Be Wrapped
import wx
from SendKeys import SendKeys

#internal
from controller import Controller, ControllerHandler




#------------------------------------------------------------------------------
#---Utility Functions
#------------------------------------------------------------------------------
#
#Current application
#
application = None

#
#
#
logWindow = None

#--
def printException():
    """
    Prints the exception information in case exception is thrown in a
    try/catch block
    """
    e = sys.exc_info ()
    sys.excepthook  ( e[0], e[1], e[2] )

    
#--
def getConfigDir(allUsers=False):
    '''
    allUsers:True : All User's configuration folder
             False: User's configuration folder
    '''
    sp = wx.StandardPaths.Get()
    if allUsers:
        cd = os.path.split(sp.GetConfigDir())[0]
    else:
        cd = sp.GetUserConfigDir()
    return cd
#--
def getUserDir(allUsers=False):
    '''
    allUsers:True : All User's 
             False: User's 
    '''
    sp = wx.StandardPaths.Get()
    if allUsers:
        cd = os.path.split(sp.GetConfigDir())[0]
    else:
        cd = sp.GetUserConfigDir()
    return os.path.split(cd)[0]
        
#--
def getAppDataDir(allUsers=False):
    sp = wx.StandardPaths.Get()
    if allUsers:
        cd = sp.GetConfigDir()
    else:
        cd = sp.GetUserDataDir()
    return cd
    
        
#--- 
def putInClipboard(text):
    '''
    Put the text to the clipboard. This should be extended to support
    other formats
    '''
    clipboard.OpenClipboard()
    clipboard.EmptyClipboard()
    clipboard.SetClipboardData(win32con.CF_UNICODETEXT, unicode(text)) 
    clipboard.CloseClipboard()
    
    
    
#---
def sendKeys(iKeys):
    '''
    '''
    SendKeys.SendKeys(iKeys)


#---
def getUser():
    '''
    '''
    return getpass.getuser()

#---
def getWindowText(iHwnd):
    return gui.GetWindowText(iHwnd)

#---
def getWindowClassName(iHwnd):
    return gui.GetClassName(iHwnd)

#---
def getWindowPID(hwnd):
    '''
    returns a tuple with process IDs for given window
    '''
    return win32process.GetWindowThreadProcessId(hwnd)
    

#---
def getClipboardText():
    '''
    '''
    clipboard.OpenClipboard()
    newData = ''
    newFormat = 0
    newFormat = clipboard.EnumClipboardFormats(newFormat)
    print newFormat
    if newFormat == win32con.CF_UNICODETEXT or newFormat == win32con.CF_TEXT:
        print 'gettting data'
        newData = clipboard.GetClipboardData(newFormat)
    clipboard.CloseClipboard()
    print 'cv: ' 
    print newData
    return newData
    
  
#--- 
def getSelectedText(keepOldData=True):
    '''Returns the selected text from the current window.
    Currently this function uses Ctrl+C hack to get the selected text
    to the clipboard and return it. It should work with most of the applications
    but not for all
    
    Also this method overrides the last clipboard state for binary content.
    It works fine if clipboard contains text data (ascii, unicode) but othercases
    old content is lost.
    '''
    
    if keepOldData and 0:
        print 'trying to keep old data'
        clipboard.OpenClipboard() 
        oldFormat = 0
        oldFormat = clipboard.EnumClipboardFormats(oldFormat)
        if oldFormat:
            oldData = clipboard.GetClipboardData(oldFormat) 
        clipboard.CloseClipboard() 
    else:
        oldFormat = 0
    
    sendKeys('^c')
    time.sleep(0.05)
    
    newData = getClipboardText()
    
    
    if oldFormat:
        clipboard.OpenClipboard()
        clipboard.EmptyClipboard()
        clipboard.SetClipboardData(oldFormat, oldData) 
        clipboard.CloseClipboard()
            
    return newData

    
#--- 
def replaceSelectedText(iNewText, keepOldData = True):
    '''Replaces the selected text with the given one in the current window. If no
    text is selected given text will be inserted in the current location
    Currently this function uses Ctrl+V hack to set the text from the 
    clipboard. It should work with most of the applications but not for all

    Also this method overrides the last clipboard state for binary content.
    It works fine if clipboard contains text data (ascii, unicode) but othercases
    old content is lost.
    '''
    if keepOldData and 0:
        clipboard.OpenClipboard() 
        oldFormat = 0
        oldFormat = clipboard.EnumClipboardFormats(oldFormat)
        if oldFormat:
            oldData = clipboard.GetClipboardData(oldFormat) 
        clipboard.CloseClipboard() 
    else:
        oldFormat = 0
    
    clipboard.OpenClipboard()
    clipboard.EmptyClipboard()
    clipboard.SetClipboardData(win32con.CF_UNICODETEXT,unicode(iNewText)) 
    clipboard.CloseClipboard()
    
    sendKeys('^v')
    
    if oldFormat:
        clipboard.OpenClipboard()
        clipboard.EmptyClipboard()
        clipboard.SetClipboardData(oldFormat, oldData) 
        clipboard.CloseClipboard()
    
    
#------------------------------------------------------------------------------
#---
#------------------------------------------------------------------------------
if __name__ == '__main__':
    print 'test nsqrPy.cmdrui'
    
