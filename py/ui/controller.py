#=============================================================================
#=== Ozgur Aydin Yuksel, 2007 (c)
#=============================================================================

#standard
import sys
import traceback


#third party
import win32con 

#To Be Wrapped
import wx
import pyHook

#internal
from common import printException, setApplication


try:
    from cmd_config import getManager
except:
    getManager = None
    
__doc__ = \
"""
Controller instance to handle windows messages without the need of a UI

evt parameter can deliver the window handle (evt.Window) and window name 
(evt.WindowName) when the event is generated. So it is possible to make something
like Enso what Enso does, we just need to keep the window handle when the application
is triggered (CapsLock key is pressed?)
"""

#=============================================================================
#===Messages to be send...
#=============================================================================

class ControllerHandler:
    if 1: #Message identifiers which are sent to controller handlers
        activated = 'activated'
        deactivated = 'deactivated'
        executed = 'executed'
        executeFailed = 'executeFailed'
    #End of Message Identifiers
    
    #---
    def __init__(self):
        pass
    #---
    def onControllerMessage(self, iMsg):
        """
        """
        pass
        
    #---
    def onTextChanged(self, iText, iLastEntry):
        """
        Will be called when the current text is changed. Here we can display it
        """
        pass
        
    #---
    def onOptionsChanged(self, iOptions):
        """
        """
        pass
        
        
    #---
    def onOptionSelectionChanged(self, iOptions, iSelection):
        """
        iOptions: A list of options
        iSelection: Index of currently selected item, might be -1 for no selection
        """
        pass


#
#
#
class BaseState (object):
    #---
    def __init__(self, controller):
        object.__init__(self)
        self.controller = controller
        self.__options = []
        self.__selectedIdx = -1
        self.__entry = ''
        self.title = []
    
    #---
    def __getOptions(self):
        return self.__options
    def __setOptions(self, options):
        self.__options = options
        try:
            self.controller.handler.optionsChanged(self.__options)
        except: 
            printException()
    options = property(__getOptions, __setOptions)
    
    #---
    def __getSelection(self):
        return self.__selectedIdx
    def __setSelection(self, selection):
        try:
            if selection != self.__selectedIdx:
                max = len(self.options)
                if selection < -1: 
                    self.__selectedIdx = max - 1
                elif selection >= max:
                    self.__selectedIdx = 0
                else:
                    self.__selectedIdx = selection 
            self.controller.handler.selectionChanged(self.__options, self.__selectedIdx)
        except: 
            printException()
    selectedIdx = property(__getSelection, __setSelection)
    
    #---
    def __getSelectionText(self):
        idx = self.selectedIdx
        if idx >= 0 and idx < len(self.options): 
            return self.options[idx]
        else:
            return ''
    selectedText = property(__getSelectionText)
        
    #---
    def __getEntry(self):
        return self.__entry
    #---
    def __setEntry(self, entry):
        try:
            select = -1
            
            if len(entry) > len(self.__entry):
                oldOptions = self.options 
            else:
                oldOptions = self.controller.manager.getOptions()
            self.__entry = entry
            
            newOptions = []
            for option in oldOptions:
                if self.findFunction(option, entry) >= 0:
                    newOptions.append(option)
            if len(newOptions) > 0:
                select = 0
            self.options = newOptions
            self.selectedIdx = select
            self.controller.handler.textChanged(self.__entry)
        except: 
            printException()

    entry = property(__getEntry, __setEntry)
    
    #--
    def __getComplatedEntry(self):
        entry = self.selectedText
        if entry == '':
            entry = self.entry
        return entry
    complatedEntry = property(__getComplatedEntry)
            
    
    
    
    #---        
    def execute(self, key):
        try: 
            self.controller.execute(self.complatedEntry, key.evt)
        except: 
            printException()
            
    def cancel(self):
        try: 
            self.controller.cancel()
        except: 
            printException()
            
    def activate(self, command):
        self.__entry = ''
        self.__options = []
        self.__selectedIdx = -1
        
    def deactivate(self):
        pass 
        
        
    def processKeys(self, key):
        #print 'processKeys: ' + str(key.id) + ' ' + str(self)
        try:
            if key.id == KeyInfo.activation:
                pass
            elif key.id == KeyInfo.cancel:
                pass
            elif key.id in KeyInfo.autoComplate:
                pass
            elif key.id in KeyInfo.ignored:
                pass
            elif key.id in KeyInfo.previous:
                self.selectedIdx -= 1
            elif key.id in KeyInfo.next:
                self.selectedIdx += 1
            elif key.id in KeyInfo.back:
                if KeyInfo.hasModifiers():
                    newText = ''
                else:
                    newText = self.entry
                    newPos = len(newText) - 1
                    if newPos >= 0:
                        newText = newText[:newPos]
                self.entry = newText
            else:
                val = key.chr
                #print (val, type(val), str(val))
                #if val.isalnum() or val.isspace():
                self.entry += val
        except:
            printException()
            
    #--
    def findFunction(self, option, entry):
        assert(None)
  
        
#
#
#
class CommandState (BaseState):
    '''
    Command State might be in quasimodal or non-quasimodal. It should handle its own states
    to handle the key evens
    '''
    def __init__ (self, controller):
        BaseState.__init__(self, controller)
        self.onKeyDown = self.__tKeyDown
        self.onKeyUp = self.__tKeyUp
        self.title = 'Start Typing...'
        
        
        
    def activate(self, command):
        '''
        Will be called when state is activated, both command and option will be empty
        Command state always start in transient mode
        
        When command state is activated it should get the command names from manager
        and update the options list
        '''
        BaseState.activate(self, command)
        assert(command == None)
        assert(self.controller.manager.command == None)
        
        self.onKeyDown = self.__tKeyDown
        self.onKeyUp = self.__tKeyUp
        
        try:
            self.options = self.controller.manager.getOptions()
        except:
            printException()
        
    def findFunction(self, option, entry):
        return option.find(entry)
        
        
    #
    # Internal States to handle key events
    #
    #---Transient State
    #---
    def __tKeyDown(self, key):
        '''
        This is a transient state, if any key down event is received, it should
        switch to Quasimodal state
        '''
        self.processKeys(key)
        #print 'Switch to Quasimodal State'
        self.onKeyDown = self.__qmKeyDown
        self.onKeyUp = self.__qmKeyUp
        return False
    #---
    def __tKeyUp(self, key):
        '''
        Since Active state is transient, here we should only receive Capslock
        Up event and switch to Non-quasimodal state
        '''
        assert(key.id == KeyInfo.activation)
        #print 'Switch to Non-Quasimodal State'
        self.onKeyDown = self.__nqmKeyDown
        self.onKeyUp = self.__nqmKeyUp
        return False
        
    #---Quasimodal State
    #---
    def __qmKeyDown(self, key):
        '''
        This is same with Non-quasimodal state, we simply process the keys
        '''
        self.processKeys(key)
        return False
    #---
    def __qmKeyUp(self, key):
        '''
        Execute only of <Capslock> Up is received, and cancel if <ESC> Up is received
        '''
        if key.id == KeyInfo.activation:
            self.execute(key)
        elif key.id == KeyInfo.cancel:
            self.cancel()
        return False
    
    #---Non-Quasimodal State
    #---
    def __nqmKeyDown(self, key):
        '''
        This is same with Quasimodal state, we simply process the keys
        '''
        self.processKeys(key)
        return False
    #---
    def __nqmKeyUp(self, key):
        '''
        Execute only of <Enter> Up is received, and cancel if <ESC> Up is received
        '''
        if key.id == KeyInfo.enter:
            self.execute(key)
        elif key.id == KeyInfo.cancel:
            self.cancel()
        return False
        
        
    
        
#
#
#
class OptionState (BaseState):
    '''Options State is non-quasimodal. It handles following special key events:
        - <Esc> Up: Deactivates the controller
        - <Enter> Up: Executes the command
    '''
        
        
    def __init___(self, controller):
        BaseState.__init__(self, controller)
        
        
        
    def activate(self, command):
        '''
        Will be called when state is activated. Command is the current command instance Option is most likely empty
        '''
        BaseState.activate(self, command)
        assert(command)
        if hasattr(command, 'internallyUsedName'):
            name = command.internallyUsedName
        else:
            name = 'XXX'
        self.title = name + '...'
        try:
            self.options = command.options
        except:
            printException()
        
    def onKeyDown(self, key):
        '''
        '''
        self.processKeys(key)
        return False
        
        
    def onKeyUp(self, key):
        '''
            <Enter> Up: Execute 
            <Esc> Up: Deactivate
        '''
        if key.id == KeyInfo.enter:
            self.execute(key)
        elif key.id == KeyInfo.cancel:
            self.cancel()
        return False
        
    def findFunction(self, option, entry):
        return option.lower().find(entry)
        
        
    
#
#
#
class KeyInfo:
    modifiers = {win32con.VK_LSHIFT:0, 
                 win32con.VK_RSHIFT:0,
                 win32con.VK_LMENU:0,
                 win32con.VK_RMENU:0,
                 win32con.VK_LCONTROL:0,
                 win32con.VK_RCONTROL:0}
                 
    autoComplate = [win32con.VK_RIGHT, win32con.VK_TAB, win32con.VK_END]
    
    previous = [win32con.VK_UP, win32con.VK_PRIOR]
    
    next = [win32con.VK_DOWN, win32con.VK_NEXT]
    
    back = [win32con.VK_LEFT, win32con.VK_BACK]
           
    ignored = [win32con.VK_HOME, win32con.VK_RETURN]
    
    activation = win32con.VK_CAPITAL
    
    cancel = win32con.VK_ESCAPE
    
    enter = win32con.VK_RETURN
    
    @classmethod
    def hasModifiers(cls):
        for key in KeyInfo.modifiers:
            if KeyInfo.modifiers[key]:
                return True
        return False
        
    def __init__(self, evt):
        self.evt = evt
        self.id = evt.KeyID
        self.chr = chr(evt.Ascii)
        
                
        
#=============================================================================
#===
#=============================================================================
class Controller (object):
    '''
    '''            
    def __init__(self, applications, manager, handler):
        '''
        '''
        self.__commandState = CommandState(self)
        self.__optionState = OptionState(self)
        self.__state = None
        
        self.applications = applications
        self.manager = manager
        self.handler = handler
        
        self.__hookManager = pyHook.HookManager()                    
        self.__hookManager.KeyDown = self.__onKeyDown
        self.__hookManager.KeyUp = self.__onKeyUp
        self.__hookManager.HookKeyboard()
        
        self.__inExecution = False
        
    #---
    def __del__(self):
        self.__hookManager.UnhookKeyboard()
    
    #---
    def __onKeyUp(self, evt):
        '''
        Key Up event is received for each key press of user. We have following cases:
            * Just return if we are in execution
            * Update modifier keys if this is a modifier one
            * Inform current state if there is one
            * Cancel activation Key up event, we don't pass key down for activation key, so no key up
        '''  
        if self.__inExecution:
            return True
            
        key = KeyInfo(evt)      
        if  KeyInfo.modifiers.has_key(key.id):
            KeyInfo.modifiers[key.id] = 0
            return True
                
        if self.__state:
            return self.__state.onKeyUp(key)
        elif key.id == KeyInfo.activation:
            return False
            
        return True
        
        
    #---    
    def __onKeyDown(self, evt):
        '''
        Key Down event is received for all key downs from user. We have following cases:
            * Just return if we are in execution
            * Update modifiers if this is a modifier key
            * Inform the current state if there is one
            * Activate command state if there is nothing and this activation key
        '''
        if self.__inExecution:
            return True
            
        key = KeyInfo(evt)
        if  KeyInfo.modifiers.has_key(key.id):
            KeyInfo.modifiers[key.id] = 1
            return True
        
        if self.__state:
            return self.__state.onKeyDown(key)
        elif key.id == KeyInfo.activation:
            self.activate(self.__commandState, evt)
            return False
        else:
            retval = True
        return retval
          
    #---
    def cancel(self):
        '''
        '''
        try:
            self.__state = None
            self.manager.command = None
            self.manager.lastWindowHandle = -1
            self.handler.deactivated()
        except:
            printException()
    
    #---
    def activate(self, state, evt):
        wx.CallLater(1, self.__activateOnTimer, state, evt)
        
    #---
    def __activateOnTimer(self, *args, **kw):
        #print '__activateOnTimer'
        try:
            evt = args[1]
            self.applications.setCurrent(evt.Window)
        except:
            printException()


        state = args[0]
        assert(state)
        if self.__state:
            self.__state.deactivate()
        self.__state = state
        self.__state.activate(self.manager.command)
        self.handler.activated(self.__state)
            
    #---
    def execute(self, entry, evt):
        wx.CallLater(1, self.__executeOnTimer, entry, evt)
        
   
    #---
    def __executeOnTimer(self, *args, **kw):
        self.__inExecution = True
        try:
            deactivate = True
            entry = args[0]
            evt = args[1]
            assert(self.__state)
            
            commandName = self.__commandState.complatedEntry
            optionName = self.__optionState.complatedEntry
            
            if self.manager.command:
                #print 'This was already in option state, so direct execution'
                assert (entry == optionName)
                self.manager.command.execute(commandName, optionName)
            else:
                #print 'This was in command state, we first need to get the command'
                if entry != '':
                    self.manager.command = entry
                    cmd = self.manager.command
                else:
                    cmd = None
                if cmd:
                    if hasattr(cmd, 'options'):
                        options = cmd.options
                    else:
                        options = None
                        
                    if options is None:
                        #print 'No Options, we execute'
                        cmd.execute(commandName, optionName)
                    else:
                        #print 'Should switch to options state'
                        deactivate = False
                        cmd.internallyUsedName = commandName
                        self.activate(self.__optionState, evt)
        except:
            deactivate = True
            printException()
            
        if deactivate:
            self.__state.deactivate()
            self.__state = None
            self.manager.command = None
            self.manager.lastWindowHandle = -1
            self.handler.deactivated()
                
        self.__inExecution = False
        
         

        
#=============================================================================
#===
#=============================================================================
if __name__ == '__main__':
    print 'ui.controller'
    import simplepanel
    simplepanel.main()
    