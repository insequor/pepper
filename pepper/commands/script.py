# coding=utf-8
"""" Run a script, for development purposes """

# Standard Imports
import logging 
import os 
from pathlib import Path
from importlib import reload 
from importlib.machinery import SourceFileLoader

# Third Party Imports

# Internal Imports 
from pepper import ui 


class Command:
    author = 'Ozgur Aydin Yuksel'
    info = '''Short cuts for taking notes'''
    
    
    #--
    def __init__(self, ui, wx, manager):
        self.manager = manager
        self.names = ["script"]
        
    #--
    def execute(self, name, option):
        match name:
            case "execute":
                try:
                    cmd = [
                        "pipenv",
                        "run",
                        "python",
                        r"spikes\script.py"
                    ]
                    logging.debug(f"Executing: {cmd}")
                    os.system(f"start cmd /k {' '.join([str(c) for c in cmd])}")
                except Exception as error:
                    logging.exception(error)
                    return False
                return True
            case "script":
                try:
                    scriptPath = Path("spikes", "script.py")
                    if 1:
                        try:
                            reload(script)
                        except Exception:
                            script = SourceFileLoader("script", str(scriptPath)).load_module()
                        script.main()
                    else:
                        with open(Path("spikes", "script.py"), "r") as file:
                            script = file.read()
                            locals_ = locals()
                            exec(script, globals(), locals_)
                            locals_["main"]()

                except Exception as error:
                    logging.exception(error)
                    return False
                return True
            case _:
                raise ValueError(f"Unknown command name '{name}'")
            

if __name__ == '__main__':
    pass
