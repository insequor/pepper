
"""
    Wrapper object to work with OneNote

    Reference pages related to the com interface:
    * https://learn.microsoft.com/en-us/office/client-developer/onenote/application-interface-onenote
    * https://github.com/varunsrin/one-py
    * https://github.com/samwyse/OnePy/blob/master/onepy.py
    
"""

#standard
import datetime
from io import StringIO
import logging
import time
from xml.etree import ElementTree

#thirdparty
import pytz
import pywintypes
import win32com as com
import win32com.client as client

#internal
from pepper.applications.defaultapplication import DefaultApplication


ElementTree._original_serialize_xml = ElementTree._serialize_xml


def serialize_xml_with_CDATA(write, elem, qnames, namespaces, short_empty_elements, **kwargs):
    if elem.tag == 'CDATA':
        write("<![CDATA[{}]]>".format(elem.text))
        return
    return ElementTree._original_serialize_xml(write, elem, qnames, namespaces, short_empty_elements, **kwargs)


ElementTree._serialize_xml = ElementTree._serialize['xml'] = serialize_xml_with_CDATA


def CDATA(text):
   element =  ElementTree.Element("CDATA")
   element.text = text
   return element


# Generate and cache the type information for the OneNote COM object
# client.gencache.EnsureDispatch("0EA692EE-BB50-4E3C-AEF0-356D91732725")
app = client.Dispatch('OneNote.Application')

# Takes in an object and returns a dictionary of its values
def parseAttributes(obj: ElementTree.Element):
    tempDict = {}
    for key,value in obj.items():
        tempDict[key] = value
    return tempDict

class MSOneNotePage (object):
    """ 
        Page represent the state of the page when the instance is created 

        In order to avoid keep requesting the data we use commit() to reflect the changes
        to the application
    """
    def __init__(self, pageId: str):
        self.content = app.GetPageContent(pageId)
        
    @property 
    def xml(self) -> ElementTree.ElementTree:
        return self.__xml
    
    @property
    def name(self):
        # return self.data['name']
        return self.xml.getroot().get("ID")
    
    @property
    def title(self):
        # return self.data['name']
        title = self.xml.getroot().find(f".//one:Title//one:T", self.__namespaces)
        if title is None:
            raise ValueError("Could not find the title element in the page content")
        print(ElementTree.tostring(title, encoding="unicode"))
        return title.text
    
    @title.setter
    def title(self, value):
        # return self.data['name']
        xml = self.xml
        xml.getroot().set("name", value)
        title = xml.getroot().find(f".//one:Title//one:T", self.__namespaces)
        title.text = "" 
        cdata = CDATA(value) 
        title.append(cdata)

        
    @property
    def content(self):
        return self.__content
    
    @content.setter
    def content(self, value):
        self.__content = value
        content = StringIO(self.__content)
        content.seek(0)
        self.__xml = ElementTree.parse(content)
        namespace = self.__xml.getroot().tag.split('}')[0][1:]
        self.__namespaces = {"one":namespace}
    
    def show(self):
        '''calls NavigateTo on the OneNote application for this object'''
        app.NavigateTo(self.xml.getroot().get("ID"))

    def commit(self):
        # TODO: No idea why I can't pass datetime.datetime.now()
        date = pytz.utc.localize(datetime.datetime(year=1899, month=12, day=30))
        value = ElementTree.tostring(self.xml.getroot(), encoding="unicode")
        value = value.replace("ns0:", "one:").replace(":ns0", ":one")
        # value = self.__content 
        # print("\n\n=====\n", value, "\n=====\n")
        app.UpdatePageContent(value, date)


#
#
class MSOneNoteSection (object):
    def __init__(self, data):
        self.data = data
        
    @property    
    def name(self):
        return self.data['name']
    
    
    @property
    def pages(self) -> list[MSOneNotePage]:
        hierarchy = app.GetHierarchy(self.data['ID'], client.constants.hsPages)
        oneTree = ElementTree.fromstring(hierarchy)
        pages = []
        for node in oneTree:
            pageId = node.get("ID")
            assert pageId
            page = MSOneNotePage(pageId)
            pages.append(page)
        return pages
    
    def page (self, name) -> MSOneNotePage:
        for page in self.pages:
            if page.name == name:
                return page 
        raise ValueError(f"Could not find the page with name '{name}'")

    def show(self):
        '''calls NavigateTo on the OneNote application for this object'''
        app.NavigateTo(self.data['ID'])
        
    def create_new_page(self):
        pageID = app.CreateNewPage(self.data['ID'])
        page = MSOneNotePage(pageID)
        return page


#
#
class MSOneNoteNotebook (object):
    def __init__(self, data):
        self.data = data
        try:
            self.data['name']
        except:
            self.data['name'] = 'Unfiled Notes'

    @property 
    def name(self):
        return self.data['name']
    
    @property 
    def sections(self) -> list[MSOneNoteSection]:
        hierarchy = app.GetHierarchy(self.data['ID'], client.constants.hsSections)
        oneTree = ElementTree.fromstring(hierarchy)
        sections = []
        for node in oneTree:
            section = MSOneNoteSection(parseAttributes(node))
            sections.append(section)
        return sections
    
    def section(self, name) -> MSOneNoteSection:
        for section in self.sections:
            if section.name == name:
                return section
        raise ValueError(f"Could not find the section with name '{name}'")
    
    def show(self):
        '''calls NavigateTo on the OneNote application for this object'''
        app.NavigateTo(self.data['ID'])


class MSOneNote (DefaultApplication):
    def __init__(self, hwnd = None):
        DefaultApplication.__init__(self, hwnd)

        # Com interface will represent all the instances of the application. Actually, there is only 
        # one application, there are multiple windows. Given hwnd refers to the handle for the window
        # TODO: What is the relation between the window handles and the hwnd we receive here?
        #       We can make sure that MSOneNote current page/current section etc can return the selected 
        #       window
        pass 
    
    @property 
    def app(self):
        # TODO: We should avoid using a global variable for the app
        return app 
    
    @property
    def notebooks(self) -> list[MSOneNoteNotebook]:
        hierarchy = app.GetHierarchy("", client.constants.hsNotebooks)
        #TODO: Handle encoding here since below code will raise error with unicode characters
        oneTree = ElementTree.fromstring(hierarchy)
        
        notebooks = []
        for notebook in oneTree:
            nbk = parseAttributes(notebook)
            notebooks.append(MSOneNoteNotebook(nbk))

        return notebooks
    
    def notebook(self, name) -> MSOneNoteNotebook:
        for notebook in self.notebooks:
            if notebook.name == name:
                return notebook
        raise ValueError(f"Could not find the notebook with name '{name}'")
                

#==============================================================================
def main():
    logging.debug("MSOneNote.py")
    one = MSOneNote()
    if 0:
        # Open the specified notebook and section
        notebook_name = "SPLM"
        section_name = "Pepper"
        page_title = "New Page Title"

        one_note = client.Dispatch("OneNote.Application.15")
        # Get the XML representation of notebooks and sections
        notebooks_xml = one_note.GetHierarchy("", client.constants.hsNotebooks)
        sections_xml = one_note.GetHierarchy("", client.constants.hsSections)

        # Process notebooks
        notebook_nodes = notebooks_xml.getElementsByTagName("one:Notebook")
        for notebook_node in notebook_nodes:
            notebook_name = notebook_node.getAttribute("name")
            print("Notebook:", notebook_name)

            # Process sections within the notebook
            section_nodes = notebook_node.getElementsByTagName("one:Section")
            for section_node in section_nodes:
                section_name = section_node.getAttribute("name")
                print("  Section:", section_name)

        # Create a new page
        new_page_id = one_note.CreateNewPage(section_id="YourSectionID")
        one_note.UpdatePageContent(new_page_id, "<one:Page ...>Your Content Here</one:Page>")

        return 
    logging.debug(f"   one: {one}")
    
    notebook = one.notebook("SPLM")
    logging.debug(f"   notebook: {notebook}")
    for section in notebook.sections:
        logging.debug(f"        section: {section.name}")
    section = notebook.section("Pepper")
    logging.debug(f"   section: {section}")
    for page in section.pages:
        logging.debug(f"        page: {page.name}")    
    # page = section.page("COMAPI")
    page = section.create_new_page()
    time.sleep(1)
    if 0:
        content = page.content.replace ("!!DATE", "This will be page title")
        content = content.replace ("!!NOTE", "This will be the note part")
        content = content.replace ("!!CONTEXT", "This will be the context part")  
    
    # page.title = "Sample Page created using pywin32"
    # page.name = "This is my new page"
    logging.debug("BEFORE MODIFICATION")
    content = page.content
    logging.debug(content)
    
    content = content.replace("!!TITLE", "This is automated 12")
    content = content.replace("!!NOTE", "This is new Note 34")
    logging.debug("AFTER MODIFICATION")
    logging.debug(content)
    page.content = content 
    time.sleep(1)
    logging.debug(f"    page content:\n{page.content}")
    page.show()

    logging.debug(f"   page: {page}")
    

if __name__ == '__main__':
    logging.basicConfig(level="DEBUG")
    main()
    