
#standard
import xml  
from xml.etree import ElementTree

#thirdparty
import win32com as com
import win32com.client

#internal


hsSelf = 0
hsNotebooks = 2
hsSections = 3
hsPages = 4

app = com.client.Dispatch('OneNote.Application')

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
        hierarchy = app.GetHierarchy(self.data['ID'], hsSections)
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
    
#
#
class MSOneNoteSection (object):
    def __init__(self, data):
        self.data = data
        
    def __get_name(self):
        return self.data['name']
    name = property(__get_name)
    
    def __get_pages(self):
        hierarchy = app.GetHierarchy(self.data['ID'], hsPages)
        oneTree = ElementTree.fromstring(hierarchy)
        pages = []
        for node in oneTree:
            page = MSOneNotePage(parseAttributes(node))
            pages.append(page)
        return pages
    pages = property(__get_pages)
    
    
    def create_new_page(self):
        pageID = app.CreateNewPage(self.data['ID'])
        hierarchy = app.GetHierarchy(pageID, hsSelf)
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
        print 'getting the content'
        return app.GetPageContent(self.data['ID'])
    def __set_content(self, value):
        print 'setting the content'
        app.UpdatePageContent(value)
    content = property(__get_content, __set_content)
    
    
#
#  
class MSOneNote (object):
    def __init__(self):
        pass
      
      
    def __get_notebooks(self):
        hierarchy = app.GetHierarchy("", hsNotebooks)
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
            print notebook.name
            if notebook.name == name:
                return notebook
                

#==============================================================================
if __name__ == '__main__':
    print 'MSOneNote.py'
    one = MSOneNote()
    for notebook in  one.notebooks:
        print notebook.name
        for section in notebook.sections:
            print '._', section.name
            for page in section.pages:
                print  '._._', page.name
                
                
    