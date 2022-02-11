#Andrew Christian
#10/10/2021

#james.maddison@constitution.gov
#jame$.maddy@the-const.is-me.com
#gb@wonder-life.com
#Billy Bags
#George Bailey

from adbook import AddressBook

#####################################################################
#Main Function

program = AddressBook()

program.openFile() #convert file to list of list data structure

while program.running == True:

    program.run_instance() #main menu selection
    
    if program.cur_op != '':
        program.cur_op.run_op() #operation selected from main menu

    program.cur_op = ''

print('\nSaving updated contacts list to file...')
print('\nProgram exiting...\n')

#####################################################################
