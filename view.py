#The menu class

from operation import Operation

class View(Operation):

    def __init__(self, adbook):
        Operation.__init__(self, adbook)
        self.type = 'View Op'
    
    #################################################################
    #Display contacts

    #Overrides super class function- different title and prints all rows
    def displayContacts(self):

        self.formatWidth()
        
        if self.adbook.total_w < 201:
            self.limit = self.adbook.total_w
        else:
            self.limit = 201

        print("\033c") #clears console screen and adds newlines after
        print(self.type)
        print('###################')
        print('## Contacts List ##')
        for n in range(0, self.limit - 1):
            print('#', end = '')
        print()

        for row in self.adbook.data:
            i = 0
            for col in row:
                print(col.rjust(self.adbook.col_wds[i]), end = ' ') #print all contact data with appropriate formatting
                i += 1
            print()

        print()

    #################################################################

    def run_op(self):
        
        self.op_running = True
        
        while self.op_running == True:
            self.displayContacts()
            self.cont_op()
