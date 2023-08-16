"""Sample site for step by step execution of graphs"""


# Standard
import logging
from pathlib import Path 
import time 

# Third Party
from fastapi import APIRouter, WebSocket, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
import web 

# Internal
from pepper.commandprompt import commander


class WebTemplate(web.template.render):
    renderPath: Path = Path(".") / "pepper" / "webserver" / 'templates'
    
    def __init__(self) -> None:
        super().__init__(WebTemplate.renderPath)

class HTMLTemplateResponse(HTMLResponse):
    def __init__(self, template):
        super().__init__(str(template))


router = APIRouter(
    prefix="/test",
    tags=["test"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def _():
    """A list of test pages"""
    return HTMLResponse("test pages")


@router.get("/commandprompt")
async def _():
    """Testing the UI for the command prompt"""
    template: WebTemplate = WebTemplate()
    commander.Manager.commandsFolder = Path("pepper", "commands")
    commander.manager.refresh()
    options = commander.manager.getOptions()
    return HTMLTemplateResponse(template.test.commandprompt(options, time.time())) 
    

if __name__ == "__main__":
    pass 
