#Delete operation class

from operation import Operation

class Delete(Operation):

    def __init__(self, adbook):
        Operation.__init__(self, adbook)
        self.type = 'Delete Op'
    
    ###############################################################
    #delete contact

    def delete_contact(self):
        
        if self.op_running == True and self.choice != -1: #The user hasn't indicated to return to search or main menu
            
            self.choice = ''
            print()

            while self.choice not in ['Y', 'N', -1]:
                self.choice = input('Delete this contact [y/n]? ')
                self.choice = self.choice.upper()
            
            if self.choice == 'Y':
                del(self.adbook.data[self.choice_rows[1]]) #the second element of choice_rows holds the row number from data[] that the matching contact came from
                print()
            else:
                self.choice = -1
                print('\nReturning to Search Menu...\n')
                #self.op_running = False

    ###############################################################
    #Run the op

    def run_op(self):
        
        self.op_running = True
        
        while self.op_running == True:
        
            self.get_criteria()
            self.get_match()
            self.displayContacts()
            self.select_match()
            self.delete_contact()
            self.cont_op()