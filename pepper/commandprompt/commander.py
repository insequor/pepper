#=============================================================================
#=== Ozgur Aydin Yuksel, 2007 (c)
#=============================================================================


#Standard Imports
from importlib import reload, import_module
from inspect import cleandoc
import logging
import os
from pathlib import Path
import sys
from typing import Any 

#Third Party Imports

#Internal Imports
from pepper import applications


__doc__ = \
"""
Commander module which defines the basic structure to define and manage commands. 


TODO
-------------------------------------
* Commands to add:
    - remember: Remember a certain location in a document, application, url with a key word
    - remind: set reminders for a certain time or duration
    - accents: accented characters in Turkish and Romanian
    - clipboard: remember old text in clipboard, good especially for code editing
    - gtd: time management commands
    - pages: switch between documents in a single application, like pages in VS

* Commands to think about:
    - tt: time tracking
          it is quite tricky to write a good one
* Commands NOT to add:
    - window: open, close, minimize windows
"""

#=============================================================================
#===
#=============================================================================

class Singleton:
    _instances = {}
    def __new__(cls, *args, **kw):
        if not cls in Singleton._instances:
            instance = super().__new__(cls)
            Singleton._instances[cls] = instance

        return Singleton._instances[cls]
   

class Manager(Singleton):
    #-- Location for command scripts are
    commandsFolder: Path
    
    #
    commandModules = {}
    
    #
    #PROPERTIES
    #
    @property 
    def command(self):
        return self.__currentCommand

    @command.setter    
    def command(self, name):
        '''
        '''
        if name == None:
            self.__currentCommand = None
            return
        
        cmd = None
        
        try:
            cmd = self.__cmdMap[name]
        except KeyError:
            logging.warning('Command is not registered for: ' + name)
            logging.debug(f"{self.__cmdMap}")
            cmd = None
        
        if cmd and hasattr(cmd, 'activated'):
            cmd.activated(name)
        
        self.__currentCommand = cmd

    @property 
    # TODO: Update the return type hint
    def commands(self) -> list[Any]:
        return [cmd for cmd, _ in self.__cmdList]
            
    #--
    def __init__(self, ui=None, wx=None, applications_deprecate=None):
        self.connection = None 

        self.ui = ui
        self.wx = wx
        # TODO: Deprecate this 
        self.applications = applications

        #- Mapping to the names to the commands
        #- It has following structure:
        #- self.__cmdMap = { name: instance }
        self.__cmdMap = {}  
        
        #-
        #- List of command classes. It has a tuple for each element, first is the
        #- class, second is the instance. Instance is deleted when refresh command
        #- is received.
        #- 
        # logging.debug("RESET COMDN LIST in Manager.__init__")
        self.__cmdList = []
        
        #Window handle which has the focus when controller is activated
        #This is assumed as the last window before controller takes the control
        self.lastWindowHandle = -1
        
        #---
        self.__currentCommand = None
        
    #--
    def addCommand(self, cmdClass):
        self.__cmdList.append([cmdClass, None])
        
    
    #---
    def getOptions(self):
        items = []
        if self.__currentCommand:
            try:
                if hasattr(self.__currentCommand, 'options'):
                    items = self.__currentCommand.options
            except Exception:
                logging.error(f"could not get options from {self.__currentCommand}")
        else:
            self.__cmdMap = {}
            for cmdPair in self.__cmdList:
                try:
                    cmdClass = cmdPair[0]
                    cmd = cmdPair[1]
                    if not cmd:
                        #print 'trying to instantiate the command'
                        cmd = cmdClass(self.ui, self.wx, self)
                        cmdPair[1] = cmd
                    names = cmd.names
                    for name in names:
                        if name in self.__cmdMap:
                            logging.warning(f"SKIP THE DUPLICATED NAME FOR NOW.... {name}")
                            # TODO: Create a unique name using the command class name)
                        else:
                            self.__cmdMap[name] = cmd
                            items.append(name)
                except Exception:
                    logging.exception(f"Problem retrieving names from {cmd}") 
            
            items.sort()
        return items
    
    #---
    def refresh(self):
        '''
        Destroy all command instances so they can be re-created next time
        '''
        # logging.debug("RESET COMDN LIST in Manager.refresh")
        self.__cmdList = []
        commands = getAvailableCommands(Manager.commandsFolder)
        for cmd in commands:
            self.addCommand(cmd)

    def sendMessage(self, msg: str, data: Any = None):
        if self.connection:
            self.connection.send({"key": msg, "data": data}) 


manager = Manager()
       

#------------------------------------------------------------------------------
#---
#------------------------------------------------------------------------------
# TODO: Return type annotation should be list of Command type
def getAvailableCommands(source: Path) -> list[Any]:
    """
        Returns a list of Command classes from given folder
        Each python file, execpt __init__.py will be loaded and Command class will 
        be retrieved. It does not check if Command class actually provides the required
        methods or derived from base class
    """
    commands = []
    if not source.is_dir():
        logging.error(f"--- given path is not directory: {source}")
    else:
        if not str(source) in sys.path:
            sys.path.append(str(source))
        for entry in source.glob("*.py"):
            if entry.stem != '__init__':
                try:
                    try:
                        if entry.stem in Manager.commandModules:
                            myModule = Manager.commandModules[entry.stem]
                            reload(myModule)
                        else:
                            myModule = import_module(entry.stem)
                            Manager.commandModules[entry.stem] = myModule
                    except Exception:
                        logging.exception("Exception during (re)loading command package")
                        continue 
                    
                    try:
                        commands.append(myModule.Command)
                    except AttributeError:
                        pass 

                except Exception:
                    logging.exception("Exception during (re)loading command package")
    return commands


#------------------------------------------------------------------------------
#---
#------------------------------------------------------------------------------
def getAvailableCommandScripts(source: Path) -> list[Path]:
    """
        Returns a list of python file names (full path)
        Each python file, execpt __init__.py will be loaded and Command class will 
        be retrieved and deleted to make sure that return list only contains the 
        possible command scripts
    """
    commands = []
    import os
    import sys
    if not source.is_dir():
        logging.error(f"--- given path is not directory: {source}")
    else:
        if not str(source) in sys.path:
            sys.path.append(str(source))
        for entry in source.glob("*.py"):
            if entry.stem != "__init__":
                try:
                    myModule = import_module(entry.stem)
                    if hasattr(myModule, "Command"):
                        commands.append(entry)
                    del myModule
                except Exception:
                    logging.exception(f"Could not load command script: {entry}")
                    pass
    return commands
        

if __name__ == '__main__':
    pass 
