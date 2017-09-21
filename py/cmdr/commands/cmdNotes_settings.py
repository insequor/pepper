

Settings = {
    #Notes are defined as note command where each key is the name of the 
    #command, and each value is the dictionary which gives name of the 
    #notebook and note of the section
    #'my note'        : {'notebook':'OneOffice', 'section':'Notes'}}
    'notes' : {}
}


try:
    from cmdNotes_settings_local import Settings 
except:
    pass