#edit contact class

from operation import Operation

class Edit(Operation):

    def __init__(self, adbook):
        Operation.__init__(self, adbook)
        self.edit_ind = -1 #holds the index of the column the new data is editing
        self.change_str = '' #string holding new data
        self.type = 'Edit op'

    #################################################################
    #edit contact

    def edit_contact(self):
        
        if self.op_running == True and self.choice != - 1: #The user hasn't indicated to return to search or main menu

            #reset for each iteration
            self.choice = ''
            self.verified = ''
            self.check = False
            
            print()
            print('Fields:')
            print('1. Name')
            print('2. E-mail1')
            print('3. E-mail2')
            print('4. Phone_Number1')
            print('5. Phone_Number2')
            print()

            #Control structure to check user hasn't indicated to quit current op
            while self.verified not in ['Y', '-1', -1]: #trying to break through layered calls...
                while self.choice not in ['1', '2', '3', '4', '5', -1]:
                    self.choice = input('Which field do you want to edit [1-5, -1 to return to Search Menu]? ')
                    if self.choice == '-1':
                        self.choice = int(self.choice)

                if self.choice == -1:
                    print('\nReturning to Search Menu...\n')
                
                #This monstrasety needs to be condensed...

                org_data = self.match_data #copy original data if changes are canceled...
                
                if self.choice == '1': #change name
                    self.choice = input('Enter change: ')
                    self.edit_ind = 0
                    self.match_data[0] = self.choice #change the name column only
                if self.choice == '2': #change e-mail 1
                    while self.check == False: 
                        self.choice = input('Enter change: ')
                        self.edit_ind = 1
                        self.match_data[1] = self.choice #change the email 1 column only
                        self.adbook.add_op.choice = self.choice
                        self.check = self.adbook.add_op.check_email_format()
                if self.choice == '3': #change e-mail 2
                    while self.check == False: 
                        self.choice = input('Enter change: ')
                        self.edit_ind = 2
                        self.match_data[2] = self.choice #change the email 2 column only
                        self.adbook.add_op.choice = self.choice
                        self.check = self.adbook.add_op.check_email_format()
                if self.choice == '4': #change phone 1
                    while self.check == False: 
                        self.choice = input('Enter change: ')
                        self.edit_ind = 3
                        self.match_data[3] = self.choice #change the phone 1 column only
                        self.adbook.add_op.choice = self.choice
                        self.check = self.adbook.add_op.check_phone_format()
                if self.choice == '5': #change phone 2
                    while self.check == False: 
                        self.choice = input('Enter change: ')
                        self.edit_ind = 4
                        self.match_data[4] = self.choice
                        self.adbook.add_op.choice = self.choice #change the phone 2 column only
                        self.check = self.adbook.add_op.check_phone_format()
                
                self.change_str = self.choice

                self.verify_info()

                if self.verified == 'Y': #trying to avoid assigning change even if verified isn't Y -- above breaks also if it is -1(i.e. return to prev menu)
                    #This may be repeating the work from above-- not needed...
                    self.match_data[self.edit_ind] = self.change_str #this points to the same memory location as the cor row in data[], change here - change there
                else:
                    self.match_data = org_data #if not verified, revert any changes made        
    
    #################################################################
    #run op

    def run_op(self):
        
        self.op_running = True
        
        while self.op_running == True:
        
            self.get_criteria()
            self.get_match()
            self.displayContacts()
            self.select_match()
            self.edit_contact()
            self.cont_op()