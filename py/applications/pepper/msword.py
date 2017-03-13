import wx
import win32gui as gui
import win32con as con
import win32com as com
import win32process as process
import pythoncom

import win32clipboard as clipboard

import SendKeys

from defaultapplication import DefaultApplication

#=============================================================================
#===
#=============================================================================

class MSWord(DefaultApplication):
    #---
    def __getSelectedText(self):
        text = ''
        if self.word:
            if self.word.ActiveWindow:
                text = self.word.ActiveWindow.Selection.Text
        return text
    def __setSelectedText(self, text):
        if self.word:
            if self.word.ActiveWindow:
                #if we assign directly to the selection, text becomes 
                #higlighted, this method inserts given text without selecting it
                #also we check if given text is None so we can cut the contents
                if text:
                    self.word.ActiveWindow.Selection.TypeText(text)
                else:
                    self.word.ActiveWindow.Selection.Text = ''
    selectedText = property(__getSelectedText, __setSelectedText)
    
    #---
    def __init__(self, hwnd = None):
        '''
        If hwnd is None, current window will be retrieved
        '''
        DefaultApplication.__init__(self, hwnd)
        
        self.word = com.client.Dispatch('Word.Application')
        return 
        
#=============================================================================
#===
#=============================================================================
if __name__ == '__main__':
    print 'msword.py'
    
    app = MSWord()
    print app.title
    print app.selectedText
    
    