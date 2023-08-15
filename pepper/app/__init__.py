"""
    Main Application
"""
# Standard Imports
from typing import Protocol, runtime_checkable
from multiprocessing.connection import PipeConnection 

# Third Party Imports

# Internal Imports

@runtime_checkable
class App(Protocol):
    """Represents the interface to define an application to work with pepper"""
    def start(self, connection: PipeConnection):
        """ Start the application """

    def stop(self):
        """ Stop the application """
        pass  


if __name__ == "__main__":
    pass 
