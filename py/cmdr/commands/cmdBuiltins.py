#=============================================================================
#=== Ozgur Aydin Yuksel, 2007 (c)
#=============================================================================

#=============================================================================
#===Configuration
#=============================================================================
#This command does not need any configuration parameters...


#=============================================================================
#===
#=============================================================================
class Command:
    author = 'Ozgur Aydin Yuksel'
    info = '''Currently only exits the Cmdr application. It should receive the 
    application name as input later.'''
    
    
    #--
    def __init__(self, ui, wx, manager):
        self.ui = ui
        self.wx = wx
        self.manager = manager
        
        self.__functions = {
            'capslock' : self.__capslock,
            'exit' : self.__exit, 
            'help' : self.__help,
            'hide log window' : self.__hideLogWindow,
            #'preferences' : self.__preferences,
            'refresh' : self.__refresh,
            'show log window' : self.__showLogWindow}
        
        self.names = self.__functions.keys()
        
    
    #---
    def __capslock(self):
        self.ui.sendKeys('{CAPSLOCK}')
        
    #---
    def __exit(self):
        self.wx.GetApp().Exit()
        
    #---
    def __help(self):
        print 'TODO: should disply help for selected command'
    
    #---
    def __hideLogWindow(self):
        self.ui.logWindow.Hide()
    
    #---
    def __refresh(self):
        self.manager.refresh()
        
    #---
    def __showLogWindow(self):
        self.ui.logWindow.Show()
        
    #--
    def execute(self, name, option):
        try:
            self.__functions[name]()
            result = True
        except:
            self.ui.printException()
            result = False
        return result


#=============================================================================
#===
#=============================================================================
if __name__ == '__main__':
    print 'nsqrPy\cmdr\cmdexit.py'
    
    
    
