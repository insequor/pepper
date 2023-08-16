# Standard Imports
from pathlib import Path

# Third Party Imports

# Internal Imports
from expect import expect, test_that, fail, todo, skip, require, warn, run
from pepper.commandprompt import commander


class CommanderTestCase:
    
    @test_that("getAvailableCommand returns empty list if the path is not valid")
    def _(_):
        commands = commander.getAvailableCommands(Path("not valid"))
        expect(commands) == []

    @test_that("getAvailableCommands returns the list of commands in our commands folder")
    def _(_):
        source = Path("pepper", "commands")
        commands = commander.getAvailableCommands(source)
        names = {entry for entry in source.glob("*.py") if not entry.stem.endswith("_settings")}
        expect(commands).length(len(names))

    @test_that("getAvailableCommandScripts returns empty list if the path is not valid")
    def _(_):
        scripts = commander.getAvailableCommandScripts(Path("not valid"))
        expect(scripts) == []

    @test_that("getAvailableCommandScripts returns the list of files in our commands folder")
    def _(_):
        source = Path("pepper", "commands")
        scripts = commander.getAvailableCommandScripts(source)
        names = {entry for entry in source.glob("*.py") if not entry.stem.endswith("_settings")}
        expect(set(scripts)) == names

    @test_that("Manager.refresh would load all the commands from given path")
    def _(_):
        commander.Manager.commandsFolder = Path("pepper", "commands")
        manager = commander.manager
        expect(manager.commands) == []
        manager.refresh()
        expect(manager.commands) != []

    @test_that("If we set an invalid command name, current command becomes None")
    def _(_):
        manager = commander.manager
        manager.command = "not known"
        expect(manager.command).is_(None)

    @test_that("If we set None as command name, current command becomes None")
    def _(_):
        manager = commander.manager
        manager.command = None
        expect(manager.command).is_(None)

    @test_that("When the current command is None, getOptions return the options from all commands")
    def _(_):
        manager = commander.manager
        manager.command = None
        expect(manager.getOptions()) != []
        
    @test_that("Once we requested the options, we can set the current command")
    def _(_):
        manager = commander.manager
        manager.command = None
        options = manager.getOptions()
        require("capslock").in_(options)
        manager.command = "capslock"
        expect(manager.command).is_not(None)
        expect(manager.command.__class__.__module__) == "builtins_"

if __name__ == "__main__":
    run()
