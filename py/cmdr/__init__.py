#=============================================================================
#=== Ozgur Aydin Yuksel, 2007 (c)
#=============================================================================


#standard
import sys
import pickle

#third party

#to be wrapped

#internal
def printException(): 
    print 'here'
    e = sys.exc_info ()
    sys.excepthook  ( e[0], e[1], e[2] )

__doc__ = \
"""
Commander module which defines the basic structure to define and manage commands. 
"""

#=============================================================================
#===
#=============================================================================
#---
class Manager (object):
    #-- Location for command scripts are
    commandsFolder = ''
    
    #
    commandModules = {}
    
    #--
    instance = None
    
    #
    #PROPERTIES
    #
    if 1:
        def __getCurrentCommand(self):
            return self.__currentCommand
        def __setCurrentCommand(self, name):
            '''
            '''
            if name == None:
                self.__currentCommand = None
                return
            
            cmd = None
            try:
                if self.__cmdMap.has_key(name):
                    cmd = self.__cmdMap[name]
                else:
                    print('Command is not registered for: ' + name)
                if cmd and hasattr(cmd, 'activated'):
                    cmd.activated(name)
            except:
                printException()
                cmd = None
            self.__currentCommand = cmd
        command = property(__getCurrentCommand, __setCurrentCommand)
            
    #--
    def __init__(self, ui, wx):
        object.__init__(self)
        
        self.ui = ui
        self.wx = wx

        #singleton instance.... I'm not sure if this is a good idea!
        Manager.instance = self
        
        #- Mapping to the names to the commands
        #- It has following structure:
        #- self.__cmdMap = { name: instance }
        self.__cmdMap = {}  
        
        #-
        #- List of command classes. It has a tuple for each element, first is the
        #- class, second is the instance. Instance is deleted when refresh command
        #- is received.
        #- 
        self.__cmdList = []
        
        #Window handle which has the focus when controller is activated
        #This is assumed as the last window before contaoller takes the control
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
            except:
                print 'could not get options from %s' % str(self.__currentCommand)
        else:
            self.__cmdMap = {}
            for cmdPair in self.__cmdList:
                try:
                    cmdClass = cmdPair[0]
                    cmd = cmdPair[1]
                    if not cmd:
                        print 'trying to instantiate the command'
                        cmd = cmdClass(self.ui, self.wx, self)
                        cmdPair[1] = cmd
                    names = cmd.names
                    for name in names:
                        if self.__cmdMap.has_key(name):
                            print 'SKIP THE DUPLICATED NAME FOR NOW.... ' + name
                            #TODO: Create a unique name using the command class name)
                        else:
                            self.__cmdMap[name] = cmd
                            items.append(name)
                except:
                    print 'Problem retrieving names from: %s' % str(cmd) 
                    printException()
            items.sort()
        return items
    
    #---
    def refresh(self):
        '''
        Destroy all command instances so they can be re-created next time
        '''
        self.__cmdList = []
        commands = getAvailableCommands(Manager.commandsFolder)
        for cmd in commands:
            self.addCommand(cmd)
        
       
#------------------------------------------------------------------------------
#---
#------------------------------------------------------------------------------
def getAvailableCommands(iPath):
    """
    Returns a list of Command classes from given folder
    Each python file, execpt __init__.py will be loaded and Command class will 
    be retrieved. It does not check if Command class actually provides the required
    methods or derived from base class
    """
    commands = []
    import os
    import sys
    if not os.path.isdir(iPath):
        print '--- given path is not directory: ' + iPath
    else:
        if not iPath in sys.path:
            sys.path.append(iPath)
        for name in os.listdir (iPath):
            name, ext = os.path.splitext(name)
            if ext == '.py' and name != '__init__':
                try:
                    failed = False
                    #We first check if the module was already loaded or not
                    if Manager.commandModules.has_key(name):
                        try:
                            exec 'myModule = ' + 'Manager.commandModules["' + name + '"]'
                            exec 'reload (myModule)'
                        except: 
                            failed = True
                    else:
                        try: 
                            exec 'import ' + name
                            exec 'myModule = ' + name
                            exec 'Manager.commandModules["' + name + '"] = myModule'
                        except: 
                            failed = True
                    if not failed:
                        exec 'try: commands.append(myModule.Command)\nexcept: print  "No Command found in %s" % str(myModule)' 
                except:
                    failed = True
                if failed:
                    print 'Can not load the command module: ' + name
                    printException()
    print 'returning found commands', len(commands)             
    return commands

#------------------------------------------------------------------------------
#---
#------------------------------------------------------------------------------
def getAvailableCommandScripts(iPath):
    """
    Returns a list of python file names (full path)
    Each python file, execpt __init__.py will be loaded and Command class will 
    be retrieved and deleted to make sure that return list only contains the 
    possible command scripts
    """
    commands = []
    import os
    import sys
    if not os.path.isdir(iPath):
        print '--- given path is not directory: ' + iPath
    else:
        if not iPath in sys.path:
            sys.path.append(iPath)
        for name in os.listdir (iPath):
            name, ext = os.path.splitext(name)
            if ext == '.py' and name != '__init__':
                try:
                    exec 'import ' + name
                    exec 'cmd = ' + name + '.Command'
                    exec 'del ' + name
                    commands.append(os.path.join(iPath, name + '.py'))
                except:
                    pass
    return commands
        
#------------------------------------------------------------------------------
#---
#------------------------------------------------------------------------------


    
#------------------------------------------------------------------------------

if __name__ == '__main__':
    print 'test cmdr'
    if 1:
        #commands = loadAvailableCommands('D:\\ozgur\\projects\\nsqrpy.google.code\\nsqrPy\\cmdr')
        commands = getAvailableCommandScripts('D:\\ozgur\\projects\\nsqrpy.google.code\\nsqrPy\\cmdr')
        print len(commands)
        for cmd in commands:
            name = str(cmd)
            print name
    else:
        import nsqrPy.cmdr
        print dir(nsqrPy.cmdr)
        print nsqrPy.cmdr.CmdRun 
    
