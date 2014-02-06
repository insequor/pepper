#=============================================================================
#=== Ozgur Aydin Yuksel, 2014 (c)
#=============================================================================

#standard

#thirdparty
import webbrowser

#internal

#=============================================================================
#===Configuration
#=============================================================================
#This command does not need any configuration parameters...


#=============================================================================
#===
#=============================================================================
class Command:
    author = 'Ozgur Aydin Yuksel'
    info = '''Short cuts for mantis PRs'''
    
    
    #--
    def __init__(self, ui, wx, manager):
        self.ui = ui
        self.wx = wx
        self.manager = manager
        
        self.__functions = {
            'prmantis': self.__pr_mantis
            , 'prmercurial': self.__pr_mercurial
            #, 'pronenote': self.__pr_onenote
        }
        
        self.names = self.__functions.keys()
    
    def __options(self):
        options = ['enter pr number']
        if 0:
            try:
                #TODO: Triggering Ctrl+C messes up the keys for some reason
                selected = self.manager.applications.current.selectedText
                #todo: verify the selected text to see if it looks like a PR number
                #otherwise we should ask user to give a PR number through UI  5456
                selected = int(selected)
                options.append(str(selected))
            except:
                pass
        return options
        
    options = property(__options)
        
    def __pr_mantis(self, option):
        webbrowser.open('http://mantis.lmsintl.com/view.php?id=%s' % option)
        
    def __pr_mercurial(self, option):
        url = '''http://homer/hgsearch/web/?messageInput=PR%3DPRNUMBER&frameworkInput=&branchInput=&authorInput=&dateFromInput=&dateToInput=&fileName=&orderFirstlyBy=date&orderFirstly=DESC&orderSecondlyBy=author&orderSecondly=DESC&search=Search'''
        
        url = url.replace('PRNUMBER', option)
        webbrowser.open(url)
        
    def __pr_onenote(self, option):
        pass
        
    #--
    def execute(self, name, option):
        print ('pr(%s, %s)' %(name, option))
        self.__functions[name](option)
        return True


#=============================================================================
#===
#=============================================================================
if __name__ == '__main__':
    print 'nsqrPy\cmdr\cmdexit.py'
    
    
    
