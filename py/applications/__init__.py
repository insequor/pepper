#=============================================================================
#=== Ozgur Aydin Yuksel, 2007 (c)
#=============================================================================

#standard

#thirdparty

#internal
ui = None #will be set by the main app

__doc__  = '''
    Applications package to deal with the wrapping of different applications
'''


#Currently active application
current = None
from msonenote import MSOneNote

#
#
#
def getOutlookApp():
    from msoutlook import MSOutlook
    return MSOutlook()

#
#
#
def setCurrent(hwnd):
    global current
    if hwnd is None:
        current = None
    
    wndText = ui.getWindowText(hwnd)
    wndClass = ui.getWindowClassName(hwnd)
        
    if 1:
        print 'DefaultApplication'
        print 'hwnd: ' + str(hwnd)
        print 'wndClass: '  + wndClass
        print 'wndText: ' + wndText
        
    if 0 and wndClass == 'wndclass_desked_gsk' and wndText.find('Microsoft Visual C++'):
        print 'MSVisualStudio'
        from msvisualstudio import MSVisualStudio
        current = MSVisualStudio(hwnd)
    elif 0 and wndClass == 'OpusApp' and wndText.find('Microsoft Word'):
        print 'MSWord'
        from msword import MSWord
        current = MSWord(hwnd)
    elif wndClass == 'rctrl_renwnd32':
        from msoutlook import MSOutlook
        current = MSOutlook(hwnd)
    else:
        from defaultapplication import DefaultApplication
        current = DefaultApplication(hwnd)
        
#=============================================================================
if __name__ == '__main__':
    print 'applications.__init__.py'