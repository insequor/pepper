#=============================================================================
#=== Ozgur Aydin Yuksel, 2007 (c)
#=============================================================================


#=============================================================================
#=== CONFIGURATION PARAMETERS
#=============================================================================

#=============================================================================
#===
#=============================================================================
import os
import wx

import codecs


database = {}

#=============================================================================
#===
#=============================================================================
class Command:
    '''
    '''
    author = 'Ozgur Aydin Yuksel'
    info = '''Add support to write non-english characters without keyboard
    layour shifting.
    Main limitation is it will rely on common short cut keys (Ctrl+C/V/P)
    '''
    
    #---
    def __getNames(self):
        names = []
        try:
            for item in self.__database.keys():
                names.append(item)
        except:
            self.ui.common.printException()
        return names
    names = property(__getNames)
    
    
    #--
    def __init__(self, ui, wx, manager):
        self.ui = ui 
        self.wx = wx 
        self.manager = manager

        self.__database = {}
        try:
            fileName = os.path.join('../data', 'datalanguages.cfg')
            fp = codecs.open(fileName, 'r', 'utf-8')
            for line in fp.readlines():
                #remove the end of line
                line = line[:len(line)-2]
                data = line.split('|')
                if len(data) == 2:
                    self.__database[data[0]] = data[1]
            fp.close()
        except:
          self.ui.common.printException()
          self.database = []
        
    #--
    def execute(self, name, option):
        result = False
        try:
            assert(self.manager.applications.current)
            if self.__database.has_key(name):
                val = self.__database[name]
                self.manager.applications.current.selectedText = val
                result = True
        except:
            self.ui.common.printException()
            result = False
        return result


#=============================================================================
#===
#=============================================================================
if __name__ == '__main__':
    print ''
    
    
    