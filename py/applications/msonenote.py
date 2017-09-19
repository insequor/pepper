
#standard
import datetime
import xml  
from xml.etree import ElementTree

#thirdparty
import pytz
import win32com as com
import win32com.client 

#internal
from defaultapplication import DefaultApplication


app = com.client.Dispatch('OneNote.Application.15')

# Takes in an object and returns a dictionary of its values
def parseAttributes(obj):
        tempDict = {}
        for key,value in obj.items():
            tempDict[key] = value
        return tempDict

#
#
class MSOneNoteNotebook (object):
    def __init__(self, data):
        self.data = data
        try:
            self.data['name']
        except:
            self.data['name'] = 'Unfiled Notes'

    def __get_name(self):
        return self.data['name']
    name = property(__get_name)
    
    def __get_sections(self):
        hierarchy = app.GetHierarchy(self.data['ID'], com.client.constants.hsSections)
        oneTree = ElementTree.fromstring(hierarchy)
        sections = []
        for node in oneTree:
            section = MSOneNoteSection(parseAttributes(node))
            sections.append(section)
        return sections
    sections = property(__get_sections)  

    def section(self, name):
        for section in self.sections:
            if section.name == name:
                return section
    
    def show(self):
        '''calls NavigateTo on the OneNote application for this object'''
        app.NavigateTo(self.data['ID'])
#
#
class MSOneNoteSection (object):
    def __init__(self, data):
        self.data = data
        
    def __get_name(self):
        return self.data['name']
    name = property(__get_name)
    
    def __get_pages(self):
        hierarchy = app.GetHierarchy(self.data['ID'], com.client.constants.hsPages)
        oneTree = ElementTree.fromstring(hierarchy)
        pages = []
        for node in oneTree:
            page = MSOneNotePage(parseAttributes(node))
            pages.append(page)
        return pages
    pages = property(__get_pages)
    
    def page (self, name):
        for page in self.pages:
            if page.name == name:
                return page 

    def show(self):
        '''calls NavigateTo on the OneNote application for this object'''
        app.NavigateTo(self.data['ID'])
        
    def create_new_page(self):
        pageID = app.CreateNewPage(self.data['ID'])
        hierarchy = app.GetHierarchy(pageID, com.client.constants.hsSelf)
        oneTree = ElementTree.fromstring(hierarchy)
        page = MSOneNotePage(parseAttributes(oneTree))
        return page
    
#
#
class MSOneNotePage (object):
    def __init__(self, data):
        self.data = data
    
    def __get_name(self):
        return self.data['name']
    name = property(__get_name)
    
    def __get_content(self):
        return app.GetPageContent(self.data['ID'])
    def __set_content(self, value):
        date = pytz.utc.localize(datetime.datetime(year=1899, month=12, day=30))
        app.UpdatePageContent(value, date)
    content = property(__get_content, __set_content)
    
    def show(self):
        '''calls NavigateTo on the OneNote application for this object'''
        app.NavigateTo(self.data['ID'])
#
#  
class MSOneNote (DefaultApplication):
    def __init__(self, hwnd = None):
        print 'MSOneNote Application Detected'
        DefaultApplication.__init__(self, hwnd)
      
      
    def __get_notebooks(self):
        hierarchy = app.GetHierarchy("", com.client.constants.hsNotebooks)
        #TODO: Handle encoding here since below code will raise error with unicode characters
        oneTree = ElementTree.fromstring(hierarchy)
        
        notebooks = []
        for notebook in oneTree:
            nbk = parseAttributes(notebook)
            notebooks.append(MSOneNoteNotebook(nbk))

        return notebooks
    notebooks = property(__get_notebooks)    
    
    def notebook(self, name):
        for notebook in self.notebooks:
            if notebook.name == name:
                return notebook
                

#==============================================================================
if __name__ == '__main__':
    print 'MSOneNote.py'
    one = MSOneNote()
    notebook = one.notebook("One")
    section = notebook.section("Welcome")
    page = section.page("COMAPI")
    content = page.content  
    page.content = content.replace("was", "still is")
                
                
    