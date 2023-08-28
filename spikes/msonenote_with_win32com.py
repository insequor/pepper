#standard
import datetime
import logging
import time
from xml.etree import ElementTree

#thirdparty
import pytz
import pywintypes
import win32com as com
import win32com.client


# internal
from pepper.applications.msonenote import MSOneNote


def traverseXML(node: ElementTree.Element, level: int = 0):
    def i_(level) -> str:
        return "   " * level
    
    print(f"{i_(level)}|{node.tag}:")
    for key, value in node.items():
        print(f"{i_(level)}|---{key} = {value}")

    if node.text is not None:
        print(f"{i_(level)}|---{node.text}")
    

    for child in node:
        traverseXML(child, level + 1)

def main():
    # Create an instance of OneNote
    one = MSOneNote()

    notebook = one.notebook("SPLM")
    section = notebook.section("Pepper")

    *_, page = section.pages 
    print("Name:", page.name)
    print("Title:", page.title)
    page.title = "I modified this again"
    # page.commit()
    
    newElement = r"""<one:Outline xmlns:one="http://schemas.microsoft.com/office/onenote/2013/onenote">
                <one:Position x="36.0" y="86.4000015258789" z="0" />
                <one:Size width="117.001953125" height="40.28314971923828" />
                <one:OEChildren>
                    <one:OE>
                        <one:T><![CDATA[This is a sample data added to test out OneNote API functionality.  Following is a list item.]]></one:T>
                    </one:OE>
                </one:OEChildren>
                <one:OEChildren indent="2">
                    <one:OE  alignment="left">
                        <one:List>
                            <one:Bullet bullet="2" fontSize="11.0" />
                        </one:List>
                        <one:T><![CDATA[A for Apple]]></one:T>
                    </one:OE>
                    <one:OE  alignment="left">
                        <one:List>
                            <one:Bullet bullet="2" fontSize="11.0" />
                        </one:List>
                        <one:T><![CDATA[B for Ball]]></one:T>
                    </one:OE>
                    <one:OE  alignment="left">
                        <one:List>
                            <one:Bullet bullet="2" fontSize="11.0" />
                        </one:List>
                        <one:T><![CDATA[C for Cat]]></one:T>
                    </one:OE>
               </one:OEChildren>
            </one:Outline>
    """
    newElementXML = ElementTree.fromstring(newElement)
    
    xml = page.xml 
    xml.getroot().append(newElementXML)
    print("Page Content:")
    traverseXML(xml.getroot(), 1)
    # ElementTree.indent(page.xmlTree)
    # print(ElementTree.tostring(xml, encoding="unicode"))
    page.commit()

if __name__ == '__main__':
    logging.basicConfig(level="DEBUG")
    main()
    