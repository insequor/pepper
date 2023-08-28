# Standard Imports
from pathlib import Path

# Third Party Imports

# Internal Imports
from expect import expect, test_that, fail, todo, skip, require, warn, run
from pepper.applications.msonenote import MSOneNote


class MSOneNoteTestCase:
    # This test is thought to be example code to show what we can access from the application
    # It does minimum validation since we do not have full control on the applications

    @classmethod
    def before_all(cls):
        cls.one = MSOneNote()
        
    @classmethod
    def after_all(cls):
        pass

    @test_that("We can get the number of windows from the application")
    def _(self):
        expect(self.one.app.Windows.Count) > 0

    @test_that("We can iterate throught the application windows using Item() or the iterator")
    def _(self):
        windows = [self.one.app.Windows.Item(i).WindowHandle for i in range(self.one.app.Windows.Count)]
        expect(windows) != []
        windows_ = [window.WindowHandle for window in self.one.app.Windows]
        expect(windows) == windows_
        print("\n======", windows)
        
    @test_that("We can get the current page from the application")
    def _(self):
        pass 

    @test_that("We can get the current window from the app")
    def _(self):
        expect(self.one.app.Windows.CurrentWindow).is_not(None)
        self.one.app.Windows.CurrentWindow.FullPageView = False 

    @test_that("We can get the list of notebooks")
    def _(self):
        notebooks = list(self.one.notebooks)
        expect(notebooks) != []

    @test_that("notebook exposes it's name")
    def _(self):
        notebooks = list(self.one.notebooks)
        first, *_, last = notebooks
        expect(first.name) != ""
        expect(last.name) != ""
        expect(first.name) != last.name

    @test_that("We can get a notebook with it's name")
    def _(self):
        notebooks = list(self.one.notebooks)
        first, *_, last = notebooks
        first_ = self.one.notebook(first.name)
        expect(first.name) == first_.name


class NotebookTestCase:
    @test_that("add test coverage")
    @todo("missing test coverage")
    def _(_):
        fail("not implemented test")


class SectionTestCase:
    @test_that("add test coverage")
    @todo("missing test coverage")
    def _(_):
        fail("not implemented test")


class PageTestCase:
    @test_that("add test coverage")
    @todo("missing test coverage")
    def _(_):
        fail("not implemented test")


if __name__ == "__main__":
    run()
