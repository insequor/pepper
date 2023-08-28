# coding=utf-8
#=============================================================================
#=== Ozgur Aydin Yuksel, 2014 (c)
#=============================================================================

#standard
import logging 

#thirdparty

#internal
from pepper import ui 
from pepper.commands.notes_settings import Settings
from pepper.applications.msonenote import MSOneNote

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
        self.manager = manager
        self.names = list(Settings['notes'])
        
    options = []
    
    #--
    def execute(self, name, option):
        option = option.strip()
        noteSettings = Settings['notes'][name]
        one = MSOneNote()
        
        notebook = one.notebook(noteSettings['notebook'])
        section = notebook.section(noteSettings['section'])
        note_page = section.create_new_page()
        
        context = ""
        if 0: # TODO: Add the clipboard text if available
            clipboardText = ui.getClipboardText()
            if clipboardText:
                context = f"Clipboard Text: {clipboardText}"

        content = note_page.content         
        # TODO: Check if the page is created usinga a template we should simply 
        # replace things around, or if we should provide our own modifications
        if content.find("!!TITLE") >= 0:
            content = content.replace("!!TITLE", option)
            content = content.replace("!!NOTE", "")
            content = content.replace("!!CONTEXT", context)
        else:
            note_page.title = option

        note_page.content = content
        note_page.commit()
        note_page.show()
        return True


#=============================================================================
#===
#=============================================================================
if __name__ == '__main__':
    pass
    
    
    
