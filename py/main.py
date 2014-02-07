

#standard
import sys
import os

#third party
import wx

#internal
import ui
from ui.common import printException, MsgRedirector, ErrorRedirector
from ui.htmlpanel import SimplePanel as GUIPanel

import cmdr
import applications

applications.ui = ui
print ui

#=============================================================================
#===
#=============================================================================

class SimplePanelFrame ( wx.Frame ):
    def __init__ (self):
        wx.Frame.__init__ (self, None, -1, 'pepper',
        #style= wx.RESIZE_BORDER|wx.FRAME_TOOL_WINDOW|wx.CAPTION|wx.STAY_ON_TOP)
        style = wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR)
        self.SetTransparent(188)
        manager = None         
        try:
            manager = cmdr.Manager(ui, wx, applications)
            manager.refresh()
        except:
            manager = None
            printException()
            
        self.panel = GUIPanel(self, manager)
        self.SetSize((800, 450))
        self.Centre()
               
        self.controller = ui.Controller(applications, manager, self.panel)    
    
    #---
    def afterCreated(self):
        self.Hide()

   
#=============================================================================
#===
#=============================================================================
class TestApp ( wx.App ):
    def __init__(self):
        wx.App.__init__(self)
        self.ProcessMessage = None
        
        
    def OnInit (self):
        try:
            self.SetAppName('nsqrCommander')
            
            global appDataFolder
            appDataFolder = 'C:\\_downloads\\_VMShared\\Projects\\GitHub_not\\pepper\\data\\'
         
            cmdr.Manager.commandsFolder = 'C:\\_downloads\\_VMShared\\Projects\\GitHub_not\\pepper\\py\\cmdr\\commands\\'
            sys.stdout = MsgRedirector ()
            sys.stderr = ErrorRedirector ()
        
            ui.logWindow = wx.Frame(None, -1, 'pepper - Log Window')
            ui.logWindow.Bind(wx.EVT_CLOSE, self.__onClosingLogWindow)
            logWnd = wx.TextCtrl(ui.logWindow, size=(0,150), style=wx.TE_MULTILINE)
            wx.Log_SetActiveTarget(wx.LogTextCtrl(logWnd))
            ui.logWindow.SetSize((600, 400))
            ui.logWindow.Show()
            
            print 'log window is activated'
            
            self.__tbIcon = wx.TaskBarIcon ()
            iconFile = appDataFolder + 'app_icon.ico'
            icon = wx.Icon (iconFile, wx.BITMAP_TYPE_ICO)
            if not self.__tbIcon.SetIcon (icon, 'nsqrCommander'):
                print 'Could not set icon.'
                
            self.Bind(wx.EVT_TASKBAR_LEFT_UP, self.__onEvtTaskbarLeftUp)
            
            self.__frame = SimplePanelFrame()
            self.__frame.Hide()
        
        except:
            self.__frame = wx.Frame(None, -1, 'FAILED!')
            logWnd = wx.TextCtrl(self.__frame, size=(0,150), style=wx.TE_MULTILINE)
            wx.Log_SetActiveTarget(wx.LogTextCtrl(logWnd))
            #nsqrPy.printException()
            self.__frame.Show ()
        
        if self.__frame:
            self.SetTopWindow (self.__frame )
        
        return True
        
    #---
    def OnExit(self):
        if self.__tbIcon:
            self.__tbIcon.RemoveIcon ()
    
    #---
    def __onEvtTaskbarLeftUp(self, evt):
        self.ExitMainLoop ()
        self.ProcessIdle ()
    
    #---
    def __onClosingLogWindow(self, evt):
        '''We override the close event for the log window so it will be hidden only'''
        ui.logWindow.Hide()







if __name__ == '__main__':
    TestApp().MainLoop()
    