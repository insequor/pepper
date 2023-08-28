#=============================================================================
#=== Ozgur Aydin Yuksel, 2007 (c)
#=============================================================================

# Standard Imports
from dataclasses import dataclass 
import logging 
from pathlib import Path 
from typing import Any 

# Third Party Imports
import win32con 
from pynput import keyboard 
import win32gui
from pywinauto.controls.hwndwrapper import HwndWrapper

# Internal Imports
from pepper import applications 
from .commander import Manager, manager


__doc__ = """
    Controller instance to handle windows messages without the need of a UI

    evt parameter can deliver the window handle (evt.Window) and window name 
    (evt.WindowName) when the event is generated. So it is possible to make something
    like Enso what Enso does, we just need to keep the window handle when the application
    is triggered (CapsLock key is pressed?)
"""

#=============================================================================
#===Messages to be send...
#=============================================================================


@dataclass(kw_only=True)
class KeyboardEvent:
    KeyID: int 
    Ascii: str 


class KeyboardListener(keyboard.Listener):
    def __init__(self):
        self.KeyDown = None 
        self.KeyUp = None 

        def win32EventFilter(msg, data):
            return self.win32EventFilter(msg, data)
        
        super().__init__(
            win32_event_filter=win32EventFilter,
            suppress=False
        ) 

    def win32EventFilter(self, msg=None, data=None):
        """ Return True if you want to process the event, otherwise False """
        propagate: tuple[bool, Any] | bool = True 
        key = self._event_to_key(msg, data.vkCode)  #type: ignore
        match key:
            case keyboard.KeyCode():
                ascii = key.char if key.char is not None else ""
            case keyboard.Key.space:
                ascii = " "
            case _:
                ascii = "" 
        evt = KeyboardEvent(KeyID=data.vkCode, Ascii=ascii)  
        match msg:
            case win32con.WM_KEYDOWN:
                if self.KeyDown:
                    propagate = self.KeyDown(evt)
            case win32con.WM_KEYUP:
                if self.KeyUp:
                    propagate = self.KeyUp(evt)
            case win32con.WM_SYSKEYDOWN | win32con.WM_SYSKEYUP:
                # This is received with windows key
                pass 
            case _:
                logging.debug(f"   Unknown Keyboard Event: {msg}")
                return
             
        if not propagate:
            self.suppress_event()  # type: ignore (It looks like this method is only available for win32)
        

class ControllerHandler:
    # Message identifiers which are sent to controller handlers
    activated = 'activated'
    deactivated = 'deactivated'
    executed = 'executed'
    executeFailed = 'executeFailed'
    
    def __init__(self):
        pass
    
    def onControllerMessage(self, iMsg):
        """
        """
        pass
        
    def onTextChanged(self, iText, iLastEntry):
        """
        Will be called when the current text is changed. Here we can display it
        """
        pass
        
    def onOptionsChanged(self, iOptions):
        """
        """
        pass
        
        
    def onOptionSelectionChanged(self, iOptions, iSelection):
        """
        iOptions: A list of options
        iSelection: Index of currently selected item, might be -1 for no selection
        """
        pass


#
#
#
class BaseState:
    
    def __init__(self, controller: "Controller"):
        object.__init__(self)
        self.controller = controller
        self.__options = []
        self.__selectedIdx = -1
        self.__entry = ''
        self.title = []
    
    @property 
    def options(self):
        return self.__options
    
    @options.setter
    def options(self, options):
        self.__options = options
        try:
            # TODO: self.controller.handler.optionsChanged(self.__options)
            self.controller.handler.onOptionsChanged(self.__options)

        except Exception as error: 
            logging.exception(error)

    @property
    def selectedIdx(self):
        return self.__selectedIdx
    @selectedIdx.setter
    def selectedIdx(self, selection):
        try:
            if selection != self.__selectedIdx:
                max = len(self.options)
                if selection < -1: 
                    self.__selectedIdx = max - 1
                elif selection >= max:
                    self.__selectedIdx = 0
                else:
                    self.__selectedIdx = selection 
            self.controller.handler.onOptionSelectionChanged(self.__options, self.__selectedIdx)
        
        except Exception as error: 
            logging.exception(error)

    @property
    def selectedText(self):
        idx = self.selectedIdx
        if idx >= 0 and idx < len(self.options): 
            return self.options[idx]
        else:
            return ''
        
    @property
    def entry(self):
        return self.__entry
    
    @entry.setter
    def entry(self, entry):
        try:
            select = -1
            
            if len(entry) > len(self.__entry):
                oldOptions = self.options 
            else:
                oldOptions = manager.getOptions()
            self.__entry = entry
            
            newOptions = []
            for option in oldOptions:
                if self.findFunction(option, entry) >= 0:
                    newOptions.append(option)
            if len(newOptions) > 0:
                select = 0
            self.options = newOptions
            self.selectedIdx = select
            # TODO: What is the second parameter? (iLastEntry)
            self.controller.handler.onTextChanged(self.__entry, None)
        except Exception as error: 
            logging.exception(error)

    @property
    def complatedEntry(self):
        entry = self.selectedText
        if entry == '':
            entry = self.entry
        return entry
    
    def execute(self, key):
        try: 
            # self.controller.execute(self.complatedEntry, key.evt)
            manager.sendMessage("execute", (self.complatedEntry, key))
        except Exception: 
            logging.exception(f"Failed to execute the action: {self.complatedEntry}")
            
    def cancel(self):
        try: 
            manager.sendMessage("cancel", None)
            # self.controller.cancel()
        except Exception as error: 
            logging.exception(error)
            
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
        except Exception as error:
            logging.exception(error)
            
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
        super().__init__(controller)
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
        super().activate(command)
        assert(command == None)
        assert(manager.command == None)
        
        self.onKeyDown = self.__tKeyDown
        self.onKeyUp = self.__tKeyUp
        
        try:
            self.options = manager.getOptions()
        except Exception as error:
            logging.exception(error)
        
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
        self.onKeyDown = self.__qmKeyDown
        self.onKeyUp = self.__qmKeyUp
        return False
    
    def __tKeyUp(self, key):
        '''
            Since Active state is transient, here we should only receive Capslock
            Up event and switch to Non-quasimodal state
        '''
        assert(key.id == KeyInfo.activation), f"{key.id} == {KeyInfo.activation}"
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
        super().__init__(controller)
        
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
        except Exception as error:
            logging.exception(error)
        
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
        
    def __init__(self, evt: KeyboardEvent):
        self.evt = evt
        self.id = evt.KeyID
        self.chr = evt.Ascii
        
#=============================================================================
#===
#=============================================================================
class Controller:
    '''
    '''            
    def __init__(self, handler: ControllerHandler):
        '''
        '''
        self.__inExecution = False 
        self.__commandState = CommandState(self)
        self.__optionState = OptionState(self)
        self.__state = None
        
        Manager.commandsFolder = Path(".", "pepper", "commands")
        manager.refresh()

        self.handler = handler
        self.keyboard_focused = None
        self.__hookManager = KeyboardListener()                    
        if self.__hookManager:
            # self.__hookManager.handler = self.processKey
            # self.__hookManager.hook(keyboard=True, mouse=False)
            self.__hookManager.KeyDown = self.__onKeyDown
            self.__hookManager.KeyUp = self.__onKeyUp
            # self.__hookManager.HookKeyboard()
        
        self.__inExecution = False
        
    @property 
    def keyboard(self) -> KeyboardListener | None :
        return self.__hookManager

    #---
    def __del__(self):
        if self.__hookManager:
            self.__hookManager.stop()
    
    #---
    def __onKeyUp(self, evt: KeyboardEvent):
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
        if  key.id in KeyInfo.modifiers:
            KeyInfo.modifiers[key.id] = False
            return True
                
        if self.__state:
            return self.__state.onKeyUp(key)
        elif key.id == KeyInfo.activation:
            return False
            
        return True
        
    #---    
    def __onKeyDown(self, evt: KeyboardEvent):
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
        if  key.id in KeyInfo.modifiers:
            KeyInfo.modifiers[key.id] = True
            return True
        
        if self.__state:
            return self.__state.onKeyDown(key)
        elif key.id == KeyInfo.activation:
            # self.activate(self.__commandState, evt)
            manager.sendMessage("activate", (None, None))
            return False
        return True

    #---
    def cancel(self):
        '''
        '''
        try:
            self.__state = None
            manager.command = None
            manager.lastWindowHandle = -1
            #TODO: self.handler.deactivated()
            if self.keyboard_focused:
                try:
                    self.keyboard_focused.set_focus()
                except Exception:
                    logging.exception("Could not set the focus back ")

            self.handler.onControllerMessage(ControllerHandler.deactivated)

        except Exception as error:
            logging.exception(error)
    
    #---
    def activate(self, state, evt):
        try:
            applications.setCurrent()
        except Exception as error:
            logging.exception(error)

        if state is None:
            state = self.__commandState
            try:
                # self.keyboard_focused = HwndWrapper(win32gui.GetFocus())
                self.keyboard_focused = HwndWrapper(win32gui.GetForegroundWindow())
                logging.debug(f"ACTIVE: Focused element: {self.keyboard_focused}")
            except Exception:
                logging.exception("could not get focus element")
                self.keyboard_focused = None 

        assert(state)
        if self.__state:
            self.__state.deactivate()
        self.__state = state
        self.__state.activate(manager.command)
        self.handler.onControllerMessage(ControllerHandler.activated)

    #---
    def execute(self, entry, evt):
        try:
            if self.keyboard_focused is not None and self.keyboard_focused.handle is not None:
                win32gui.SetForegroundWindow(self.keyboard_focused.handle)
        except Exception:
            logging.exception("Could not set the foreground object")
        self.__inExecution = True
        try:
            deactivate = True
            assert(self.__state)
            
            commandName = self.__commandState.complatedEntry
            optionName = self.__optionState.complatedEntry
            
            if manager.command:
                #print 'This was already in option state, so direct execution'
                # assert (entry == optionName)
                manager.command.execute(commandName, entry)
            else:
                #print 'This was in command state, we first need to get the command'
                if entry != '':
                    manager.command = entry
                    cmd = manager.command
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
        except Exception as error:
            deactivate = True
            logging.exception(error)
            
        if deactivate:
            if self.__state:
                self.__state.deactivate()
                self.__state = None
            manager.command = None
            manager.lastWindowHandle = -1
            self.handler.onControllerMessage(ControllerHandler.deactivated)

        self.__inExecution = False
        
         

        
#=============================================================================
#===
#=============================================================================
if __name__ == '__main__':
    pass 
