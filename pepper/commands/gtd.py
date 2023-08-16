#=============================================================================
#=== Ozgur Aydin Yuksel, 2007 (c)
#=============================================================================

import datetime
import logging 

#=============================================================================
#===Configuration
#=============================================================================
#This command does not need any configuration parameters...

#=============================================================================
#===
#=============================================================================

class TaskStatus:
    NotStarted = 0
    InProgress = 1
    Complated = 2
    WaitingFor = 3
    Deferred = 4
    
class Command:
    author = 'Ozgur Aydin Yuksel'
    info = '''Commands to ease the GDT at work environment'''

    #--
    def __init__(self, ui, wx, manager):
        self.ui = ui 
        self.wx = wx 
        self.manager = manager 
        
        self.names = ['gtd']
        self.__options = {}
        
    #---
    @property
    def options(self) -> list[str]:
        return list(self.__options.keys())
        
    def activated(self, name):
        app = self.manager.applications.current
        self.__options = {}
        
        outlookApp = None
        try: 
            if app.IsOutlook: 
                outlookApp = app
        except: 
            outlookApp = None
            
        options = {}
        if outlookApp:
            if outlookApp.getSelectedTask():
                options = {'move task to action list' : self.__moveToActionList,
                                 'move task to master list' : self.__moveToMasterList,
                                 'move task to incubation list' : self.__moveToIncubationList,
                                 'move task to waiting for list' : self.__moveToWaitingList,
                                 'create new action item from task' : self.__createActionItem}
                                 
            elif outlookApp.getSelectedMail():
                options = {'create task to action list' : self.__createTaskToActionList,
                                 'create task to master list' : self.__createTaskToMasterList,
                                 'create task to incubation list' : self.__createTaskToIncubationList,
                                 'create task to waiting for list' : self.__createTaskToWaitingList}
            else:
                options = {}
            
            viewNames = ['Action List', 
                          'Master List',
                          'Incubation List',
                          'Waiting for List',
                          'To-Do List',
                          'Completed']
                      
            for name in viewNames:
                try: 
                    view = app.outlook.ActiveExplorer().CurrentFolder.Views.Item(name)
                    if view:
                        options['Show ' + name] = self.__getShowTaskViewFunction(name)
                except Exception as error: 
                    logging.exception(error)
                    pass
        
        
        pr = self.__getMantisPR(app)
        if pr:
            options['Mantis to Action List'] = self.__getMantisToActionListFunction(pr)
            options['Mantis to Master List'] = self.__getMantisToMasterListFunction(pr)
            options['Mantis to Incubation List'] = self.__getMantisToIncubationListFunction(pr)
            options['Mantis to Waiting List'] = self.__getMantisToWaitingListFunction(pr)
            
            
            
        self.__options = options
        
    #--
    def execute(self, name, option):
        logging.debug("execute ({name}, {option})")
        
        try:
            self.__options[option]()
            result = True
        except Exception as error:
            logging.exception(error)
            result = False
        return result
    
    #---
    def __getMantisPR(self, app):
        #IE Title         : 0119855: FEM Acoresp fails with no meaningful message - Mantis - Windows Internet Explorer
        #FF Title        :  0119855: FEM Acoresp fails with no meaningful message - Mantis - Mozilla Firefox
        #Chrome Title : 0119855: FEM Acoresp fails with no meaningful message - Mantis - Google Chrome
        title = app.title
        
        #Title should have: <PRNO>:<PR SUmmary> - Mantis - Browser Name
        try: prNo = int(title[:7])
        except: return
        
        if title[7] != ':':
            return
            
        pos = title.rfind(' - Mantis')
        if pos <= 0:
            return
            
        prSummary = title[9: pos]
        return {'no':prNo, 'summary':prSummary}
        
    def __getMantisToActionListFunction(self, pr):
        def function():
            task = createMantisTask(pr, self.manager)
            moveTaskToActionList(task)
        return function
    
    def __getMantisToMasterListFunction(self, pr):
        def function():
            task = createMantisTask(pr, self.manager)
            moveTaskToMasterList(task)
        return function
        
    def __getMantisToIncubationListFunction(self, pr):
        def function():
            task = createMantisTask(pr, self.manager)
            moveTaskToIncubationList(task)
        return function
        
    def __getMantisToWaitingListFunction(self, pr):
        def function():
            task = createMantisTask(pr, self.manager)    
            moveTaskToWaitingList(task)
        return function
        
    #---
    def __getShowTaskViewFunction(self, name):
        def showView():
            app = self.manager.applications.current
            view = app.outlook.ActiveExplorer().CurrentFolder.Views.Item(name)
            view.Apply()
        return showView
    
    #---
    def __moveToActionList(self):
        app = self.manager.applications.current
        for task in app.getSelectedTasks():
            moveTaskToActionList(task)
            task.Save()
        
    #---
    def __moveToMasterList(self):
        app = self.manager.applications.current
        for task in app.getSelectedTasks():
            moveTaskToMasterList(task)
            task.Save()
        
    #---
    def __moveToIncubationList(self):
        app = self.manager.applications.current
        for task in app.getSelectedTasks():
            moveTaskToIncubationList(task)
            task.Save()
        
    #---
    def __moveToWaitingList(self):
        app = self.manager.applications.current
        for task in app.getSelectedTasks():
            moveTaskToWaitingList(task)
            task.Save()
        
    #---
    def __createActionItem(self):
        app = self.manager.applications.current
        oldTask = app.getSelectedTask()
        task = app.createTask()
        
        task.Subject = oldTask.Subject
        task.Body = '''
        === SOURCE TASK INFORMATION ===
        Subject: %s 
        url:outlook:%s
        ''' % (oldTask.Subject, oldTask.EntryID)
        
        task.Status = TaskStatus.NotStarted
        task.StartDate = datetime.datetime.now()
        task.DueDate = task.StartDate
        
    #---
    def __createTaskToActionList(self):
        task = self.__createTaskFromMail()
        moveTaskToActionList(task)
        
    #---
    def __createTaskToMasterList(self):
        task = self.__createTaskFromMail()
        moveTaskToMasterList(task)
        
    #---
    def __createTaskToIncubationList(self):
        task = self.__createTaskFromMail()
        moveTaskToIncubationList(task)
        
    #---
    def __createTaskToWaitingList(self):
        task = self.__createTaskFromMail()
        moveTaskToWaitingList(task)
    
    def __createTaskFromMail(self):
        app = self.manager.applications.current
        mail = app.getSelectedMail()
        task = app.createTask()
        
        task.Subject = mail.Subject
        task.Body = '''
        === SOURCE E-MAIL INFORMATION ===
        Subject: %s 
        From: %s 
        To: %s 
        Sent On: %s 
        url:outlook:%s
        ''' % (mail.Subject, mail.SenderName, mail.To, mail.SentOn, mail.EntryID)
        return task
        
#=============================================================================
#=== Internal Methods
#=============================================================================        
def createMantisTask(pr, manager):
    app = manager.applications.getOutlookApp()
    
    prNo = pr['no']
    prSummary = pr['summary']
    
    task = app.outlook.CreateItem(3)
    
    task.Subject = str(prNo) + ': ' + prSummary
    task.Body = '''
    === SOURCE PR INFORMATION ===
    PR Number: %i 
    Summary: %s 
    url: http://mantis/view.php?id=%i
    ''' % (prNo, prSummary, prNo)
    task.Display()
    return task
    
def moveTaskToActionList(task):
    if task.Status == TaskStatus.Deferred or task.Status == TaskStatus.WaitingFor:
        task.Status = TaskStatus.NotStarted
    task.StartDate = datetime.datetime.now()
    task.DueDate = task.StartDate
    
def moveTaskToMasterList(task):
    if task.Status == TaskStatus.Deferred or task.Status == TaskStatus.WaitingFor:
        task.Status = TaskStatus.NotStarted
    task.StartDate = '1/1/4501'
    task.DueDate = task.StartDate
    
def moveTaskToIncubationList(task):
    task.Status = TaskStatus.Deferred
    task.DueDate = task.StartDate
    
def moveTaskToWaitingList(task):
    task.Status = TaskStatus.WaitingFor
    task.DueDate = task.StartDate
    
        
#=============================================================================
#===
#=============================================================================
if __name__ == '__main__':
    pass
    
    
    
