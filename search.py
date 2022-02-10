#Search class

from operation import Operation

class Search(Operation):
    
    def __init__(self, adbook):
        Operation.__init__(self,adbook)
        self.type = 'Search Op'
    
    ###################################################################################
    #Run the operation
    
    def run_op(self):

        self.op_running = True
        
        while self.op_running == True:
        
            self.get_criteria()
            self.get_match()
            self.displayContacts()
            self.cont_op()

    ###################################################################################