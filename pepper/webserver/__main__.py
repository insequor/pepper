"""
"""
# Standard Imports
import logging
import multiprocessing
import os 

# Third Party Imports
from fastapi import FastAPI
from uvicorn import Config, Server
from nicegui import ui

# Internal Imports
from pepper import webserver as ws


def main():
    ws.main()

if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    main()
