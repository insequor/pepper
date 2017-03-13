#=============================================================================
#=== Ozgur Aydin Yuksel, 2014 (c)
#=============================================================================

#standard

#thirdparty
import webbrowser

#internal

__doc__ = '''
PR related commands targeted to ease the work with PRs

TODO - 
-------------------
* Remember the last entered PRs (keep a limit so list does not grow)
* Store Visual Studio Bookmarks and Break Points in PR notes
* Have "switch" functionality, so when the developer switches to a PR (or a story) VS automatically 
  updates the breakpoints and bookmarks from the notes.

TODO - Mantis
-------------------

TODO - Mercurial
-------------------

TODO - OneNote
-------------------
* Get the PR Information from Mantis
* Search existing PR in all notebook, not only in open PRs section. 

'''
#=============================================================================
#===Configuration
#=============================================================================
notebook_name = 'PRs'
section_name = 'Open'
max_recent_prs = 5

#=============================================================================
#===
#=============================================================================
class _Command:
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
            , 'pronenote': self.__pr_onenote
        }
        
        self.names = self.__functions.keys()
        
        self.recentPRs = []
    
    def __options(self):
        options = ['enter pr number']
        
        options = options + self.recentPRs
        
        prNo, summary = getMantisPRFromBrowser(self.manager.applications.current)
        if prNo:
            prNo = str(prNo)
            if not prNo in self.recentPRs:
                options.append(prNo) 
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
        options.reverse()
        return options
        
    options = property(__options)
        
    def __pr_mantis(self, option):
        webbrowser.open('http://mantis.lmsintl.com/view.php?id=%s' % option)
        
    def __pr_mercurial(self, option):
        url = '''http://homer/hgsearch/web/?messageInput=PR%3DPRNUMBER&frameworkInput=&branchInput=&authorInput=&dateFromInput=&dateToInput=&fileName=&orderFirstlyBy=date&orderFirstly=DESC&orderSecondlyBy=author&orderSecondly=DESC&search=Search'''
        
        url = url.replace('PRNUMBER', option)
        webbrowser.open(url)
        
    def __pr_onenote(self, option):
        prNo, summary = getMantisPRFromBrowser(self.manager.applications.current)
        try:
            if int(prNo) != int(option):
                summary = ''
        except:
            summary = ''
            
        one = self.manager.applications.MSOneNote()
        notebook = one.notebook(notebook_name)
        section = notebook.section(section_name)
        titleStart = 'PR' + option
        prPage = None
        for page in section.pages:
            if page.name.startswith(titleStart):
                prPage = page
                break
        if not prPage:
            prPage = section.create_new_page()
            content = prPage.content.replace('PRNUMBER', option)
            content = content.replace('PRSUMMARY', summary)
            prPage.content = content
        prPage.show()
        
    #--
    def execute(self, name, option):
        option = option.strip()
        if not option in self.recentPRs:
            self.recentPRs.append(option)
            if len(self.recentPRs) > max_recent_prs:
                self.recentPRs = self.recentPRs[1:]
                
        self.__functions[name](option)
        return True

def getMantisPRFromBrowser(app):
        #IE Title         : 0119855: FEM Acoresp fails with no meaningful message - Mantis - Windows Internet Explorer
        #FF Title        :  0119855: FEM Acoresp fails with no meaningful message - Mantis - Mozilla Firefox
        #Chrome Title : 0119855: FEM Acoresp fails with no meaningful message - Mantis - Google Chrome
        title = app.title
        
        #Title should have: <PRNO>:<PR SUmmary> - Mantis - Browser Name
        try: prNo = int(title[:7])
        except: return (None, None)
        
        if title[7] != ':':
            return (None, None)
            
        pos = title.rfind(' - Mantis')
        if pos <= 0:
            return (None, None)
            
        prSummary = title[9: pos]
        return prNo, prSummary
        
#=============================================================================
#===
#=============================================================================
if __name__ == '__main__':
    print 'nsqrPy\cmdr\cmdexit.py'
    
    
    
