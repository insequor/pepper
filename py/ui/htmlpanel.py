#=============================================================================
#=== Ozgur Aydin Yuksel, 2008 (c)
#=============================================================================
#standard


#third party

#To Be Wrapped
import wx
import  wx.html as  html


#internal

#
#HTML Text Formatter
#
class HTMLFormatter:
    #
    __start = '''
    <html xmlns="http://www.w3.org/1999/xhtml">
        <body bgcolor="#666666" style="text-align: center">
            <font color="#FFFFFF" size=+4>
    '''
    #
    __end = '''
            </font>
        </body>
    </html>
    '''
    
    #
    @classmethod
    def formatText(cls, text):
        return HTMLFormatter.__start + text + HTMLFormatter.__end
  
#
#Simple HTML Window
#
class HTMLWindow(html.HtmlWindow):
    def __init__ (self, parent):
        style = wx.NO_FULL_REPAINT_ON_RESIZE
        html.HtmlWindow.__init__(self, parent, -1, style=style)
        
    #
    def setText(self, text):
        htmlText = HTMLFormatter.formatText(text)
        self.SetPage(htmlText)




#=============================================================================
#===
#=============================================================================
class SimplePanel (wx.Panel):
    def __init__(self, parent, manager):
        wx.Panel.__init__(self, parent)
        
        sizer = wx.BoxSizer(wx.VERTICAL) 
        self.__htmlWnd = HTMLWindow(self)       
        sizer.Add(self.__htmlWnd, 1, wx.EXPAND)
        
        self.SetSizer(sizer)
        sizer.SetSizeHints(self)
        self.__title = ''
        self.__lastEntry = ''
        self.__commandLine = ''
        self.__listLines = []
        self.__selectedIdx = -1
        
        #last start index to display the options
        self.__startIdx = -1
        
        
    if 1: #---HANDLER CALLS TO RECEIVE NOTIFICATIONS FROM CONTROLLER
        #
        def activated(self, state):
            assert(state)
            self.__title = state.title
            self.__commandLine = ''
            self.__lastEntry = ''
            self.__selectedIdx = -1
            self.__startIdx = -1
            self.__refresh()
            self.GetParent().Show()
        #
        def deactivated(self):
            self.GetParent().Hide()
            self.__commandLine = ''
            self.__lastEntry = ''
            
        #---
        def optionsChanged(self, options):
            '''
            '''
            self.__listLines = options
            self.__startIdx = -1
            self.__refresh()
            #print 'htmlwnd.optionsChanged'
            
        #---
        def textChanged(self, entry):
            '''
            '''
            #print 'textChanged: [%s]' % entry
            self.__commandLine = entry
            self.__lastEntry = entry
            self.__refresh()
            
        #---
        def selectionChanged(self, options, selection):
            '''
            options: A list of options
            selection: Index of currently selected item, might be -1 for no selection
            '''
            #print 'html.selectionChanged [%d]' % selection
            self.__selectedIdx = selection
            self.__refresh()
            
        ##
        ##
        #---
        def onControllerMessage(self, iMsg):
            '''
            '''
            if iMsg == cmdrui.ControllerHandler.deactivated:
                self.GetParent().Hide()
            elif iMsg == cmdrui.ControllerHandler.activated:
                self.GetParent().Show()
            self.__commandLine = ''
            self.__lastEntry = ''
            #self.__refresh()
            #print 'htmlwnd.onControllerMessage'
        #---
        def onTextChangedOld(self, iText, iLastEntry):
            '''
            Will be called when the current text is changed. Here we can display it
            '''
            print 'onTextChanged: ' + str((iText, iLastEntry))
              
            self.__commandLine = iText
            self.__lastEntry = iLastEntry
            self.__refresh()
            
        #---
        def onTextChanged(self, command, option):
            '''
            Will be called when the current text is changed. Here we can display it
            '''
            print 'onTexChanged: ' + str((command, option))
            if option != '':
                text = option
                self.__title = command + '...'
            else:
                text = command
                self.__title = 'Start Typing...'
            self.__commandLine = text
            self.__lastEntry = text
            self.__refresh()
            
        #---
        def onOptionsChanged(self, iOptions):
            '''
            '''
            self.__listLines = iOptions
            self.__startIdx = -1
            self.__refresh()
            #print 'htmlwnd.onOptionsChanged'
            
            
        #---
        def onOptionSelectionChanged(self, iOptions, iSelection):
            '''
            iOptions: A list of options
            iSelection: Index of currently selected item, might be -1 for no selection
            '''
            self.__selectedIdx = iSelection
            self.__refresh()
                
    #---END OF HANDLER CALLS 
    #
    def __refresh(self):
        # Title first
        text = '<font size="+6">' + self.__title + '<hr><br>'
        
        # Then the user entry line
        if self.__commandLine != '':
            text += self.__commandLine
        else:
            text += '<br>'
        text +='</font>'
        
        #end the options
        replText = '<font color=#0000FF>' + self.__lastEntry + '</font>'
        start = self.__startIdx
        if self.__selectedIdx < start:
            start = self.__selectedIdx
        if start == -1:
            start = 0
        count = 9
        if self.__selectedIdx - start > count - 1:
            start = self.__selectedIdx - count + 1
        self.__startIdx = start
        end = start + count
        if end >= len(self.__listLines):
            end = len(self.__listLines)
         
        for idx in range(start, end):
            item = self.__listLines[idx].replace(' ', ' ')
            item = self.__replaceSelected(item, self.__lastEntry)
            if idx == self.__selectedIdx:
                item = '<font color=#00FF00>' + item + '</font>'
            text +=  '<br>' + item
        if end < len(self.__listLines) :
            text += '<br>...'
            
        self.__htmlWnd.setText(text)
    
    #
    def __replaceSelected(self, text, selected):
        '''
        This method can be improved using re module but currently works just fine
        It does sort of case insensitive replacement. Search is based on lower 
        characters. It preserves the original cases from found string while replacing
        '''
        start = text.lower().find(selected.lower())
        if (start == -1):
            return text
        end = start + len(selected)
        return text[:start] + '<font color=#0000FF>' + text[start:end] + '</font>' + text[end:]
        
    
        
#=============================================================================
#===
#=============================================================================
if __name__ == '__main__':
    print 'htmlpanel.py provides a panel with html window for output'
    