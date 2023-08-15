"""
"""
# Standard Imports
import logging
import os

# Third Party Imports 
import webview
import keyboard 

# Internal Imports
from pepper import commandprompt  as cp 
def main():
    cp.main() 

if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    main()
