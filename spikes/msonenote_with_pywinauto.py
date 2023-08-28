"""
    Sample script, not working
    Starting code is from chatgpt but I need to work on it
"""

# Standard Imports
import logging 
import time


# Third Party Imports
from pywinauto import Application


# Internal Imports 


def main():
    # Path to the OneNote executable
    onenote_exe_path = r"C:\Program Files (x86)\Microsoft Office\root\Office16\ONENOTE.EXE"  # Replace with your actual path

    # Start OneNote
    app = Application(backend="uia").start(onenote_exe_path)
    time.sleep(2)  # Wait for OneNote to start
    logging.debug(f"app: {app}")
    
    # Connect to the running OneNote application
    main_window = app.window(title_re=".*OneNote")
    logging.debug(f"main_window: {main_window}")

    # Click on the "Notebooks" button to open the notebook list
    main_window.child_window(title="Add Page", control_type="Button").click()

    # Locate and select the target notebook and section
    notebook_name = "SPLM"
    section_name = "Pepper"

    notebook_tree = app.window(title="Notebooks and Sections")
    notebook_tree.child_window(title=notebook_name, control_type="TreeItem").click()
    notebook_tree.child_window(title=section_name, control_type="TreeItem").click()

    # Switch focus to the main OneNote window
    main_window.set_focus()

    # Send the text to the page
    page_text = "Hello, this is the content of the new page."
    main_window.type_keys(page_text)

    # Save the page
    main_window.child_window(title="File", control_type="Button").click()
    main_window.child_window(title="Save As", control_type="MenuItem").click()

    # Wait for the "Save As" dialog to appear
    save_as_dialog = app.window(title="Save As")

    # Fill in the file name and choose the save location
    save_as_dialog.child_window(control_type="Edit").type_keys("NewPage")
    save_as_dialog.Save.click()

    # Close OneNote
    main_window.close()

 


if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    main()
