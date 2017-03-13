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

class MSOutlook(DefaultApplication):
    #---
    
    #---
    def __init__(self, hwnd = None):
        '''
        If hwnd is None, current window will be retrieved
        '''
        self.IsOutlook = True
        
        print 'MSOutlook Application Detected'
        DefaultApplication.__init__(self, hwnd)
        
        self.outlook = com.client.Dispatch('Outlook.Application')
        
    def __getSelectedItem(self):
        if not self.outlook:
            return
        if self.outlook.ActiveExplorer().Selection.Count <= 0:
            return
            
        item = self.outlook.ActiveExplorer().Selection.Item(1)
        return item
        
    def getSelectedTask(self):
        item = self.__getSelectedItem()
        if item and item.Class == 48:
            return item
            
            
    def getSelectedTasks(self):
        if not self.outlook:
            return
        
        #We are not using yield here and instead return the full array since
        #if the caller modifies the objects, selection might change and our 
        #iteration might be invalid
        tasks = []
        for i in range(self.outlook.ActiveExplorer().Selection.Count):
            item = self.outlook.ActiveExplorer().Selection.Item(i + 1)
            if item and item.Class == 48:
                tasks.append(item)
        return tasks
        
    def getSelectedMail(self):
        item = self.__getSelectedItem()
        if item and item.Class == 43:
            return item
    def createTask(self):
        
        if not self.outlook:
            return
            
        item = self.outlook.CreateItem(3)
        item.Display()
        return item
        
        
        
#=============================================================================
#===
#=============================================================================
if __name__ == '__main__':
    print 'msoutlook.py'
    
    