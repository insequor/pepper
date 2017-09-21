# coding=utf-8
#=============================================================================
#=== Ozgur Aydin Yuksel, 2014 (c)
#=============================================================================

#standard

#thirdparty
import webbrowser

#internal
from cmdNotes_settings import Settings

__doc__ = '''
'''
#=============================================================================
#===Configuration
#=============================================================================


#=============================================================================
#===
#=============================================================================
class Command:
    author = 'Ozgur Aydin Yuksel'
    info = '''Short cuts for taking notes'''
    
    
    #--
    def __init__(self, ui, wx, manager):
        self.ui = ui
        self.wx = wx
        self.manager = manager
        
        self.names = Settings['notes'].keys()
        
    options = []
    
    #--
    def execute(self, name, option):
        option = option.strip()
        noteSettings = Settings['notes'][name]
        one = self.manager.applications.MSOneNote()
        
        notebook = one.notebook(noteSettings['notebook'])
        section = notebook.section(noteSettings['section'])
        note_page = section.create_new_page()
        content = note_page.content 
        content = content.replace("!!TITLE", option[:40])
        content = content.replace("!!NOTE", option)

        context = ""
        if 1: #Add the clipboard text if available
            wx = self.wx 
            if wx.TheClipboard.Open():
                if wx.TheClipboard.IsSupported(wx.DataFormat(wx.DF_TEXT)):
                    data = wx.TextDataObject()
                    wx.TheClipboard.GetData(data)
                    text = data.GetText()
                    context += "Clipboard Text: " + text 
                wx.TheClipboard.Close()
        content = content.replace("!!CONTEXT", context)
        note_page.content = content
        note_page.show()
        return True

#=============================================================================
#===
#=============================================================================
if __name__ == '__main__':
    pass
    
    
    
