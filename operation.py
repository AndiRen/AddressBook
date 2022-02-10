#operation superclass

class Operation:

    def __init__(self, adbook):
        self.adbook = adbook #be able to access adbooks functions and variables
        self.choice = '' #user choice
        self.verified = '' #user indicates data entered is correct
        self.check = False #used for control strucuter around verifiying data entry
        self.line = '' #holds prompts
        self.criteria = '' #the user input to do the search
        self.query_type = '' #which column the user is searching in
        self.search_cols = [] #which columns of the data structure the user's search will be done in
        self.row_matches = []
        self.choice_rows = []
        self.match_data = [] 
        self.row_count = 0
        self.col_count = 0
        self.limit = 0 #used with range function
        self.index = 0 #used to create a column of row numbers for matching data in searches
        self.match_range = []
        self.rowstr = ''
        self.colstr = ''
        self.op_running = False
        self.type = '' #the type of operation being done
    
    ################################################################
    #Check if user want's to continue doing current op
    
    def cont_op(self):

        #Control structure to check if user had indicated completion of op sometime during op run
        if self.choice == -1 or (self.adbook.edit_op.verified == '-1' and self.type != 'View Op'): #need to account for cross-object calls...
            if self.type == 'Add Op': #When add op, the -1 indicates return to main menu
                self.op_running = False
            else:
                pass #otherwise -1 indicated return to search menu of op, not to automatically close op run
        else:
            self.choice = '' #need to reset for next iteration

        #Ensure that user enters a valid choice to either continue or discontinue op
        while self.op_running == True and self.choice not in ['Y', 'N', -1]: 
            self.choice = input('Continue with ' + self.type + ' [y/n]? ' )
            self.choice = self.choice.upper()
        
        if self.choice == 'N': #discontinue op run, return to main menu
            self.op_running = False

    ###################################################################################
    #Gather user input for search criteria

    def get_criteria(self):

        print("\033c") #clears console screen and adds newlines after
        print(self.type) #So user is aware of what operation they are in for the search
        print('################################')
        print('##       Search Options       ##')
        print('################################')
        print('# 1. Name                      #')
        print('# 2. E-mail                    #')
        print('# 3. Phone Number              #')
        print('# 4. Return to Operations Menu #')
        print('################################')
        print()

        self.choice = ''
        self.criteria = ''
        self.search_cols = []

        #Control Strucuter to ensure only a valid menu option is selected
        while self.choice not in ['1', '2', '3', '4']:
            self.choice = input('Select search method: ')
            if self.choice not in ['1', '2', '3', '4']:
                print('\nPlease enter an integer between 1 and 4...\n')

        #Display promopts based on what type of data user chose to search and designate the range of columns to search in
        if self.choice == '1':
            self.line = 'Enter the name or partial name of the contact: '
            self.query_type = 'name contains -'
            self.search_cols = [0, 0]
        if self.choice == '2':
            self.line = 'Enter the e-mail or partial e-mail of the contact: '
            self.query_type = 'e-mail contains -'
            self.search_cols = [1, 2]
        if self.choice == '3':
            self.line = 'Enter the phone number or partial phone number of the contact: '
            self.query_type = 'phone contains -'
            self.search_cols = [3, 4]
        if self.choice == '4':
            self.line = 'Returning to Operations Menu...'
            self.op_running = False

        #Control structure ensuring that the user inputs something to use to search, uses apporpriate prompt
        while self.op_running == True and self.criteria == '':
            self.criteria = input(self.line)
    
    ###################################################################################
    #check for matches

    def get_match(self):

        if self.op_running == True: #needed to pass through nested function calls

            #WARNING -- There is no adbook.col_data. However, maybe this temporarily created it?? It somehow works though...
            self.adbook.col_data = list(zip(*self.adbook.data)) #get updated data
            self.row_matches = [] #collects the row number of all the rows that match the query

            for n in range(self.search_cols[0], self.search_cols[1] + 1): #for every column that matches the search critera type
                self.row_count = 0
                for row in self.adbook.col_data[n]: # see if there are any matches for the criteria in the given data column
                    if self.criteria.upper() in self.adbook.col_data[n][self.row_count].upper():
                        self.row_matches.append(self.row_count) #collect the row number of the data that matches the query 
                    self.row_count += 1
    
    ###################################################################################
    #extract columns and get columns max width
    
    def formatWidth(self):

        #Reset all formatting
        #WARNING -- There is no adbook.col_data. However, maybe this temporarily created it?? It somehow works though...
        self.adbook.col_data = list(zip(*self.adbook.data))
        self.adbook.col_wds.clear()
        self.adbook.total_w = 0

        for col in self.adbook.col_data:
            self.row_count = 0
            self.adbook.grt_w = 0
            for row in col:
                self.rowstr = str(row)
                if len(self.rowstr) > self.adbook.grt_w: #find the max width of each column
                    self.adbook.grt_w = len(self.rowstr)
                self.row_count += 1
            self.adbook.col_wds.append(self.adbook.grt_w + 4) #create a list of all column max widths
            self.adbook.total_w += (self.adbook.grt_w + 5) #get to total width of the columns
    
    #################################################################
    def displayContacts(self):

        if self.op_running == True:
        
            self.formatWidth()
            
            #For printing ######
            if self.adbook.total_w < 201: #don't print more # than the window has space for, i.e ~200
                self.limit = self.adbook.total_w #print enough ##### to create a top row above the data
            else:
                self.limit = 200

            print("\033c") #clears console screen and adds newlines after
            print(self.type) #show the user the type of op being run
            print('Search Criteria:', self.query_type, self.criteria) #show the user the search criteria the input
            print()
            print('#######################')
            print('## Matching Contacts ##')
            for n in range(0, self.limit): #print a row of ##### above the data
                print('#', end = '')
            print()

            self.match_data = [] #collect the matching data to be displayed
            self.row_count = 0
            self.index = 0
            for row in self.adbook.data:
                if self.row_count == 0 or self.row_count in self.row_matches: #if its the header row or the row number of a matching row comes up
                    self.col_count = 0
                    for col in row: #print all the column data of that matching row
                        if self.col_count == 0: #before the first data column add a row count column 
                            print(self.index, end = '    ')
                        colstr = str(col) #to avoid any issues with numeric data
                        print(colstr.ljust(self.adbook.col_wds[self.col_count]), end = ' ') #add proper formatting/spacing to the columns 
                        self.col_count += 1
                    self.match_data.append(row) ##### add the matching data to a list to be selected from/manipulated by user
                    self.index += 1
                    print() #newline after every row of matching data
                self.row_count += 1

            print()

    #################################################################
    #Select the correct match from search

    def select_match(self):

        self.choice = 0
        complete = False
        self.match_range = []

        for n in range(1, self.index): #make the match_range equal to the number of rows of matching data
            self.match_range.append(n)

        while self.op_running == True and complete == False:
            while self.choice not in self.match_range: #the user must choose from the list of displayed matches
                self.choice = input('Select the row number of the correct match [-1 to return to Search Menu]: ')
                try: #to avoid errors in int conversion if user did not input a number
                    self.choice = int(self.choice)
                except:
                    continue
                if self.choice == -1: #exit op if user indicated to do so
                    break
            
            if self.choice == -1: #continue to break out of op layers
                break

            self.choice_rows = [self.choice, self.row_matches[self.choice - 1]] #get the row of the contact from search match as well as original row number in data[]

            print('\nYou have selected the contact in row:', self.choice, '\n')
            
            #Control sturucture to ensure user selected the matching data that they intended to
            self.choice = ''
            while self.choice not in ['Y', 'N']:
                self.choice = input('Is this the correct contact [y/n]? ')
                self.choice = self.choice.upper()

            if self.choice == 'Y':
                self.match_data = self.match_data[self.choice_rows[0]] #reassign match_data[] to just the info from the correct match
                complete = True
            else:
                print() #for formatting

    ###############################################################
    #Verify info

    def verify_info(self):

        #Control structure to pass through rest of op if user has indicated to quit op
        if self.choice in [-1, '-1'] or self.adbook.edit_op.verified in [-1, '-1']: #trying to pass through layered function calls from multiple objects...
            self.verified = '-1' #if indicated to return to prev menu, make verified neither y/n, i.e. break out of layered calls of it
        else:
            self.verified = ''
            
            print('\nVerify contact information...\n')

            for i in self.match_data: #### delete??
                print(i)

            print()

        while self.verified not in ['Y', 'N', '-1'] and self.choice != -1 and self.adbook.edit_op.verified not in ['-1']: # added the -1 check - trying to pass through layered calls
            
            if self.adbook.edit_op.verified == 'Y': #added because of switching between objects when doing edit/verify functions
                self.verified = 'Y'
            else: 
                if self.adbook.cur_op.type == 'Add Op': #add op returns to Operations Menu, not Search Menu
                    self.verified = input('Is this information correct [y/n, -1 to return to Operations Menu]? ')
                else:
                    self.verified = input('Is this information correct [y/n, -1 to return to Search Menu]? ') ##### edits/del - return to search
                self.verified = self.verified.upper()
        
            if self.verified == 'Y' and self.adbook.edit_op.verified != 'Y': #to avoid double printing as layered functions come back up...
                print('\nAdding new data to list...\n')

            elif self.verified == 'N':
                print('\nYou chose to modify an input field...\n')
                self.adbook.edit_op.op_running = self.op_running ##### needs to be told True, since jumping in without 'starting' this objecs run_op
                self.adbook.edit_op.match_data = self.match_data ##### needs to be copied over, since this object has its own version
                self.adbook.edit_op.edit_contact() #Move into edit_op object to use its edit() function if mistake in changes to new contact data
                self.verified = ''
            elif self.verified == '-1':
                self.choice = -1

    ###############################################################
   