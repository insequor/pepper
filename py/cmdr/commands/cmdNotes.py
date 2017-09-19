# coding=utf-8
#=============================================================================
#=== Ozgur Aydin Yuksel, 2014 (c)
#=============================================================================

#standard

#thirdparty
import webbrowser

#internal

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
        
        self.__functions = {
              'note': self.__note
            , 'life lesson': self.__life_lesson
            , 'shared note': self.__shared_note 
        }
        
        self.names = self.__functions.keys()
        
    options = []
        
    def __note(self, option):
        print 'Note: ', option
        
    def __life_lesson(self, option):
        print 'Life Lesson: ', option

    def __shared_note(self, option):
        print 'Shared Note: ', option
        one = self.manager.applications.MSOneNote()
        
        notebook = one.notebook("Notebook")
        section = notebook.section("Ozgur")
        note_page = section.create_new_page()
        content = note_page.content 
        content = content.replace("!!TITLE", option[:40])
        content = content.replace("!!NOTE", option)
        content = content.replace("!!CONTEXT", "Context information is not automatically added yet")
        note_page.content = content
        note_page.show()

        
    #--
    def execute(self, name, option):
        option = option.strip()
        self.__functions[name](option)
        return True

#=============================================================================
#===
#=============================================================================
if __name__ == '__main__':
    pass
    
    
    
