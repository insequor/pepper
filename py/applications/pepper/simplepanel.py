#=============================================================================
#=== Ozgur Aydin Yuksel, 2007 (c)
#=============================================================================

import wx

import nsqrPy
import nsqrPy.wx 
import nsqrPy.cmdr as cmdr
import nsqrPy.cmdrui as cmdrui

#=============================================================================
#===
#=============================================================================
class SimplePanel (wx.Panel, cmdrui.ControllerHandler):
    def __init__(self, parent, manager):
        wx.Panel.__init__(self, parent)
        cmdrui.ControllerHandler.__init__(self)
        
        sizer = wx.BoxSizer(wx.VERTICAL)        
        self.textCtrl = wx.TextCtrl(self, \
            style = wx.TE_PROCESS_ENTER | wx.TE_PROCESS_TAB)
        sizer.Add(self.textCtrl, 0, wx.EXPAND)
        
        self.listBox = wx.ListBox(self, style =  wx.LB_SINGLE)
        sizer.Add(self.listBox, 1, wx.EXPAND)
        
        if 0:
            self.logWnd = wx.TextCtrl(self, size=(0,150), style=wx.TE_MULTILINE)
            wx.Log_SetActiveTarget(wx.LogTextCtrl(self.logWnd))
            sizer.Add(self.logWnd, 1, wx.EXPAND)
        
        font = self.textCtrl.GetFont()
        font.SetPointSize(14)
        self.textCtrl.SetFont(font)
        self.listBox.SetFont(font)
        
        self.SetSizer(sizer)
        sizer.SetSizeHints(self)
        
    if 1: #---HANDLER CALLS TO RECEIVE NOTIFICATIONS FROM CONTROLLER
        #---
        def onControllerMessage(self, iMsg):
            """
            """
            print 'onControllerMessage: ' + iMsg
            if iMsg == cmdrui.ControllerHandler.deactivated:
                self.GetParent().Hide()
            elif iMsg == cmdrui.ControllerHandler.activated:
                self.GetParent().Show()
        #---
        def onTextChanged(self, iText, iLastEntry):
            """
            Will be called when the current text is changed. Here we can display it
            """
            self.textCtrl.SetValue(iText)
            self.textCtrl.SetInsertionPointEnd()
            
        #---
        def onOptionsChanged(self, iOptions):
            """
            """
            self.listBox.Clear()
            for item in iOptions:
                self.listBox.Append(item)
            self.listBox.SetSelection(wx.NOT_FOUND)
            
            
        #---
        def onOptionSelectionChanged(self, iOptions, iSelection):
            """
            iOptions: A list of options
            iSelection: Index of currently selected item, might be -1 for no selection
            """
            if iSelection < 0 or iSelection >= len(iOptions):
                select = wx.NOT_FOUND
            else:
                select = iSelection
            self.listBox.SetSelection(select)
                
    #---END OF HANDLER CALLS 
    
    
    
#=============================================================================
#===
#=============================================================================
class TestFrame ( wx.Frame ):
    def __init__ (self, app):
        wx.Frame.__init__ (self, None, -1, 'nsqrCommander-SimplePanel',
        style= wx.RESIZE_BORDER|wx.FRAME_TOOL_WINDOW|wx.CAPTION|wx.STAY_ON_TOP)
        
        try:
            if len(sys.argv) == 2:
                cmdFolder = sys.argv[1]
            else:
                cmdFolder = os.path.dirname (sys.argv[0]) + os.sep + 'commands'
                
            manager = cmdr.Manager()          
            commands = cmdr.getAvailableCommands(cmdFolder)
            for cmd in commands:
                manager.addCommand(cmd, None, str(cmd))
        except:
            manager = None
            nsqrPy.printException()
        
        self.panel = SimplePanel(self, manager)
        self.SetSize((500, 300))
        self.Centre()
        
        self.controller = cmdrui.Controller(manager, self.panel)    
          
    #---
    def afterCreated(self):
        self.Hide()
    
            
#=============================================================================
#===
#=============================================================================
def main():
    try:
        import os
        import sys
        sys.argv.append('D:\\ozgur\\projects\\nsqrpy.google.code\\nsqrPy\\cmdr')
        nsqrPy.wx.createTestApp(TestFrame)
    except:
        nsqrPy.printException()    
        
#=============================================================================
#===
#=============================================================================
if __name__ == '__main__':
    main()
    