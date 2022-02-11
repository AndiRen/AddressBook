#Address Book class

from view import View
from search import Search
from add import Add
from edit import Edit
from delete import Delete

#####################################################################

class AddressBook:

    def __init__(self):
        self.file_name = 'contacts.txt'
        self.file = ''
        self.data = [] #list of list data structure
        self.row_elements = [] #used while creating data structure
        self.col_wds = [] #column widths for formatting
        self.grt_w = 0 #holds a given column's max width
        self.total_w = 0 #total width of all columns
        self.userChoice = ''
        self.line_str = '' #holds user input prompts 
        self.limit = 0 #used for working with range function
        self.col_count = 0
        self.running = True
        self.cur_op = ''
        self.view_op = View(self)
        self.search_op = Search(self)
        self.add_op = Add(self)
        self.edit_op = Edit(self)
        self.delete_op = Delete(self)

    #################################################################
    #open file and created list of list data strucure

    def openFile(self):

        try:
            self.file = open(self.file_name)
            print('\nAddress Book open...')
        except:
            print('File not Found')
            exit(-1)

        self.data = []

        for line in self.file:
            line = line.rstrip()
            self.row_elements = line.split(',')
            self.data.append(self.row_elements)

        self.file.close()
 
    #################################################################
    #Disaply operations Menu
    def opMenu(self):
        
        print("\033c") #clears console screen and adds newline after

        print('###########################')
        print('##    Operations Menu    ##')
        print('###########################')
        print('# 1. View contacts list   #')
        print('# 2. Search for a contact #')
        print('# 3. Add a contact        #')
        print('# 4. Edit a contact       #')
        print('# 5. Delete a contact     #')
        print('# 6. Exit program         #')
        print('###########################')
        print()

        self.userChoice = ''
        
        while self.userChoice not in ['1', '2', '3', '4', '5', '6']:
            self.userChoice = input('Select the operation you wish to perform [1-6]: ')
            if self.userChoice not in ['1', '2', '3', '4', '5', '6']:
                print('\nPlease enter an integer between 1 and 6...\n')

    #################################################################
    #Process user choice

    def processChoice(self):
        
        if self.userChoice == '1':
            self.cur_op = self.view_op
        if self.userChoice == '2':
            self.cur_op = self.search_op
        if self.userChoice == '3':
            self.cur_op = self.add_op
        if self.userChoice == '4':
            self.cur_op =self.edit_op
        if self.userChoice == '5':
            self.cur_op = self.delete_op
        if self.userChoice == '6':
            #write file function executed
            self.save_file()
            self.running = False

    #################################################################
    #Write current data to file

    def save_file(self):

        self.file = open(self.file_name, 'w')

        self.limit = len(self.data[0]) - 1 # -1 because I want one less than the last index
        #print(len(self.data[0]))

        for row in self.data:
            self.line_str = ''
            self.col_count = 0
            for col in row:
                if self.col_count < self.limit:
                    self.line_str += (col + ',') #for each row in the data structure, add each column's data
                else:
                    self.line_str += col #avoid adding extra , at the end of the line which creates phantom columns when column opened next use
                self.col_count += 1
            self.line_str += '\n'
            #print(self.line_str) #####
            self.file.write(self.line_str)
            
        self.file.close()

    ###################################################################################
    #Run program instance

    def run_instance(self):

        self.opMenu()
        self.processChoice()

    #################################################################  
#####################################################################