#=============================================================================
#=== Ozgur Aydin Yuksel, 2007 (c)
#=============================================================================


#=============================================================================
#=== CONFIGURATION PARAMETERS
#=============================================================================

#=============================================================================
#===
#=============================================================================
# Standard Imports
import codecs
import logging
import os
from pathlib import Path

# Third Party Imports

# Internal Imports
from pepper import applications


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
    @property
    def names(self) -> list[str]:
        return list(self.__database.keys())
    
    #--
    def __init__(self, ui, wx, manager):
        self.manager = manager

        self.__database = {}
        try:
            fileName = Path("data", "datalanguages.cfg")
            fp = codecs.open(str(fileName), 'r', 'utf-8')
            for line in fp.readlines():
                #remove the end of line
                line = line[:len(line)-2]
                data = line.split('|')
                if len(data) == 2:
                    self.__database[data[0]] = data[1]
            fp.close()
        except Exception as error:
          logging.exception(error)
          self.database = []
        
    #--
    def execute(self, name, option):
        result = False
        try:
            assert(applications.current)
            if name in self.__database:
                val = self.__database[name]
                logging.debug(f"ACCENTS.execute {name} => {val}")
                applications.current.selectedText = val
                result = True
        except Exception as error:
            logging.exception(error)
            result = False
        return result


#=============================================================================
#===
#=============================================================================
if __name__ == '__main__':
    pass
