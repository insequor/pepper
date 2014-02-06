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
def setCurrent(hwnd):
    global current
    if hwnd is None:
        current = None
    
    print ui
    wndText = ui.getWindowText(hwnd)
    wndClass = ui.getWindowClassName(hwnd)
        
    if 0:
        
        #print wndText
        #print wndClass
        if wndClass == 'wndclass_desked_gsk' and wndText.find('Microsoft Visual C++'):
            print 'MSVisualStudio'
            from msvisualstudio import MSVisualStudio
            current = MSVisualStudio(hwnd)
        elif wndClass == 'OpusApp' and wndText.find('Microsoft Word'):
            print 'MSWord'
            from msword import MSWord
            current = MSWord(hwnd)
        elif wndClass == 'rctrl_renwnd32':
            from msoutlook import MSOutlook
            current = MSOutlook(hwnd)
    else:
        if 1:
            print 'DefaultApplication'
            print 'hwnd: ' + str(hwnd)
            print 'wndClass: '  + wndClass
            print 'wndText: ' + wndText
        from defaultapplication import DefaultApplication
        current = DefaultApplication(hwnd)
        
#=============================================================================
if __name__ == '__main__':
    print 'applications.__init__.py'