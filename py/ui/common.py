#standard

#third party
import wx

#internal

def printException():
    print 'printException'
    
    
def setApplication(wnd):
    print 'setApplication'
    
#------------------------------------------------------------------------------
#--- Message redicting for wxLogger
#------------------------------------------------------------------------------
class Redirector :
    def __init__ ( self ):
        pass
    def write(self, text):
        if text == '\n': #--looks like print sends end of line seperately
            return
        self.printText (text)
    def write(self, text, tags=(), mark='insert'):
        l = len(text)
        if l > 0 and text[l-1] == '\n':
            text = text[:l-1]
        if len(text) > 0:
            self.printText (text)
        
    def writelines(self, l):
        map(self.write, l)
        
    def printText ( self, text ): pass
    
    def flush(self): pass
        
class MsgRedirector ( Redirector ):
    def __init__ ( self ):
        Redirector.__init__ ( self )
        
    def printText ( self, text ):
        wx.LogMessage ( text )
        
class ErrorRedirector ( Redirector ):
    def __init__ ( self ):
        Redirector.__init__ ( self )
        
    def printText ( self, text ):
        wx.LogError ( text )