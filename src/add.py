#Add contact class

from operation import Operation

###################################################################################

class Add(Operation):

    def __init__(self, adbook):
        Operation.__init__(self, adbook)
        #self.name = ''
        #self.email = ''
        #self.phone = ''
        self.notallowed = ['(', ')', '\\', '[', ']', ',', '<', '>', ':', ';']
        self.repeats = ['!!', '##', '$$', '%' + '%', '^^', '&&', '**', '--', '__', '..', '||', '++', '==', '~~', '``', '??', '{' + '{', '}' + '}']
        self.domcheck = '' #to do special check of domain portion of email
        self.stripped = '' #removes formatting from phone number
        self.parts = [] #to hold different parts of email address for checking format
        self.type = 'Add Op'

###################################################################################
    ###############################################################
    #Enter new contact info

    def get_info(self):
        
        print("\033c") #clears console screen and adds newlines after
        print('###############################')
        print('##        Add Contact        ##')
        print('###############################')
        print()

        # add these to reset when coming back in for a new add
        self.check = False
        self.match_data = [] #hold the data for the new contact, reusing variable from search operation
        self.choice = '' 
        self.verified = '' 
        self.adbook.edit_op.choice = '' 
        self.adbook.edit_op.verified = ''

        #Enter name
        self.choice = input('Enter the name of the contact: ')
        self.match_data.append(self.choice)
        
        #Enter email
        for n in range(0, 2):
            if n == 0: 
                line = 'Enter the contact\'s primary email: '
            if n == 1:
                line = 'Enter the contact\'s secondary email: '
            while self.check == False:
                self.choice = input(line)
                self.check_email_format()

            self.match_data.append(self.choice)
            self.check = False

        #enter phone number
        for n in range(0, 2):
            if n == 0: 
                line = 'Enter the contact\'s primary phone number [xxx-xxx-xxxx format]: '
            if n == 1:
                line = 'Enter the contact\'s secondary phone number [xxx-xxx-xxxx format]: '
            while self.check == False:
                self.choice = input(line)
                self.check_phone_format()
    
            self.match_data.append(self.choice)
            self.check = False
       
    ###############################################################
    #Verify e-mail format
    def check_email_format(self):
        
        self.check = False
        
        try: #otherwise caused error when entry had no @ character
            self.parts = self.choice.split('@') #split e-mail address into two parts by the @ (for this reason, I restrict only one use of @)
            self.domcheck = self.parts[1].replace('-', '') #for checking that the top-domain only has alphanumeric and - or . characters
            self.domcheck = self.domcheck.replace('.', '')
        except:
            self.parts = ['*', '*'] #purely arbitarary to assign them this -- just so I know the @ is missing
        
        #Formatting- There is an @ and . -- the @ comes before the last occurance of .
        #None of the not-allowed characters are used and no special character is immediately repeated, i.e. no ## or ..
        #No special characters begin the email address or are the characer before the @ -- Domain name has only alphanumeric, -, or . characters
        #The domain name ends with com, gov, net, or edu -- Recipient name length <= 64, domain name length <= 253
        if self.choice.count('@') == 1 and '.' in self.choice and self.choice.index('@') < self.choice.rindex('.')\
        and any(char in self.notallowed for char in self.choice) == False and any(elem in self.choice for elem in self.repeats) == False\
        and self.choice[0].isalnum() and self.parts[0][-1].isalnum() and self.domcheck.isalnum() and (self.choice.endswith('org')\
        or self.choice.endswith('com') or self.choice.endswith('gov') or self.choice.endswith('net') or self.choice.endswith('edu'))\
        and len(self.parts[0]) < 65 and len(self.parts[1]) < 254:
            self.check = True
        if self.choice == '': # blank entries, i.e. skipping allowed
            self.check = True
        if self.check == False:
            print('\nincorrect e-mail format...\n')
        
        return self.check #needed to add this for other classes using function -- very messy, should clean up so that this class also uses return...

    ###############################################################
    #verify phone number format
    def check_phone_format(self):
        
        self.check = False

        self.stripped = self.choice #copy the original input
        self.stripped = self.stripped.replace('-', '') #get rid of formatting
        if len(self.choice) == 12 and self.choice[3] == '-' and self.choice[7] == '-' and self.stripped.isnumeric(): #check proper format
            self.check = True
        if self.choice == '': # blank entries, i.e. skipping allowed
            self.check = True
        if self.check == False:
            print('\nincorrect phone number format...\n')
        
        return self.check #needed to add this for other classes using function -- very messy, should clean up so that this class also uses return...

    ###############################################################
    #Add the contact to the datastructure

    def add_contact(self):

        if self.verified == 'Y' and self.choice != -1: #The user hasn't indicated to return to search and verified info is good to add
            self.adbook.data.append(self.match_data)
        else:
            pass
    
    ###############################################################
    #Run the operation

    def run_op(self):

        self.op_running = True

        while self.op_running == True:
            
            self.get_info()
            self.verify_info()
            self.add_contact()
            self.cont_op()

###################################################################################